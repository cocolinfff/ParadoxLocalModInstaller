
import sqlite3
import random
import getpass
import zipfile
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import shutil
import threading
import urllib.request
import ssl

def CreateMod(pos, name):
    file = open(pos + 'mod/' + name + '.mod', 'w')
    file.write(f'''version="*.*.*"
tags={{
    "Font"
}}
name="{name}"
supported_version="9.9.9"
path="{pos}mod/{name}"''')
    file = open(pos + 'mod/' + name + '/descriptor.mod', 'w')
    file.write(f'''version="*.*.*"
tags={{
    "Font"
}}
name="{name}"
supported_version="9.9.9"
path="{pos}mod/{name}"
picture="thumbnail.png"''')

def insertSQL(name, Default=1, NewAddress=""):
    conn = sqlite3.connect(pos + 'launcher-v2.sqlite')
    c = conn.cursor()
    ModAddress = "mod/" + name + ".mod"
    RandomID = '''0e65a352-015d-478a-b08a-''' + str(random.randint(100000000000, 900000000000))
    if Default:
        FileAddress = "C:\\Users\\" + user + "\\Documents\\Paradox Interactive\\Stellaris\\mod\\" + name
    else:
        FileAddress = NewAddress + "\\" + name

    c.execute(f'''SELECT * FROM mods WHERE displayName = "{name}"''')
    result = c.fetchone()
    if result:
        print("Item already exists in the database.")
        return
    else:
        c.execute(f'''INSERT INTO mods (id,pdxId,steamId,gameRegistryId,name,displayName,descriptionDeprecated,thumbnailUrl,thumbnailPath,version,tags,requiredVersion,arch,os,repositoryPath,dirPath,archivePath,status,source,cause,timeUpdated,isNew,createdDate,subscribedDate,size,metadataId,remotePdxId,remoteSteamId,metadataVersion,isMetadataApplied,metadataStatus,metadataGameId)    VALUES ("{RandomID}",NULL,NULL,"{ModAddress}",NULL,"{name}",NULL,NULL,NULL,"*.*.*",NULL,"3.7.4",NULL,NULL,NULL,"{FileAddress}",NULL,"ready_to_play","local","",NULL,1,1683392067,NULL,69,NULL,NULL,NULL,NULL,0,"not_applied",NULL )''')

    conn.commit()
    print("SQL Inserted")
    conn.close()

def zipExtract(Filename, name, Default=1, NewAddress=''):
    if Default:
        save_path = pos + 'mod/' + name 
    else:
        save_path = NewAddress + '/' + name

    # Check if the directory already exists
    if os.path.exists(save_path):
        # Remove the existing directory and its contents
        shutil.rmtree(save_path)

    # Extract the zip file
    file = zipfile.ZipFile(Filename)
    file.extractall(save_path)
    file.close()
    MoveFile(save_path)
def MoveFile(temp_dir):
# Check if the descriptor.mod file exists in the target directory
    if not os.path.exists(os.path.join(temp_dir, 'descriptor.mod')):
        # Get the list of subdirectories in the target directory
        subdirectories = [f for f in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, f))]
        # Move all files from the subdirectories to the target directory
        for subdir in subdirectories:
            subdir_path = os.path.join(temp_dir, subdir)
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                shutil.move(file_path, temp_dir)
            os.rmdir(subdir_path)
def download_and_install():
    mod_url = "https://github.com/cocolinfff/Ethics-Civics-Infinity-new/archive/refs/heads/master.zip"  # Replace with the actual URL of the mod
    mod_name = "ECI_local_test"  # Replace with the name of the mod

    # Define a function to download and install the mod
    def download_and_install_mod():
        # Download the mod file
        try:
            #temp_dir = os.path.join(os.getcwd(), 'temp')
            #os.makedirs(temp_dir, exist_ok=True)
            #mod_filename = os.path.join(temp_dir, mod_name + ".zip")
            def update_progress(count, block_size, total_size):
                progress = count * block_size * 100 / total_size
                progress_bar['value'] = progress
                root.update_idletasks()
            print(mod_name)
            urllib.request.urlretrieve(mod_url, mod_name+'.zip', reporthook=update_progress)
        except urllib.error.URLError:
            messagebox.showerror("Error", "Failed to download the mod!")
            return

        # Install the mod
        insertSQL(mod_name)
        zipExtract(mod_name + ".zip", mod_name)
        CreateMod(pos, mod_name)
        messagebox.showinfo("Success", "Mod downloaded and installed successfully!")

    # Create a new thread to run the download_and_install_mod function
    thread = threading.Thread(target=download_and_install_mod)
    thread.start()

# Rest of the code...

def run_program():
    filename = entry_filename.get()
    name = entry_name.get()

    if filename and name:
        progress_bar.start()
        insertSQL(name)
        progress_bar.step(25)
        zipExtract(filename, name)
        progress_bar.step(50)
        CreateMod(pos, name)
        progress_bar.step(75)
        progress_bar.stop()
        messagebox.showinfo("Success", "Mod created successfully!")
    else:
        messagebox.showerror("Error", "Please enter both filename and MOD name.")
ssl._create_default_https_context = ssl._create_unverified_context
user = getpass.getuser()
pos = "C:/Users/" + user + "/Documents/Paradox Interactive/Stellaris/"
root = tk.Tk()
root.title("Mod Creator")
root.geometry("400x400")

label_filename = tk.Label(root, text="Select your MOD File(zip):")
label_filename.pack()

entry_filename = tk.Entry(root)
entry_filename.pack()

button_browse = tk.Button(root, text="Browse", command=lambda: entry_filename.insert(tk.END, filedialog.askopenfilename()))
button_browse.pack()

label_name = tk.Label(root, text="MOD name:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

button_run = tk.Button(root, text="Install mod", command=run_program)
button_run.pack()

output_label = tk.Label(root, text="")
output_label.pack()

progress_bar = ttk.Progressbar(root, mode='determinate')
progress_bar.pack()

button_download = tk.Button(root, text="一键操作：Download ECI From Github and Install", command=download_and_install)
button_download.pack()
button_download.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

root.mainloop()
