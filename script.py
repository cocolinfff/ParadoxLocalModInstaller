import sqlite3
import random
import getpass
import zipfile
import os
import tkinter as tk
from tkinter import filedialog
def CreateMod(pos,name):
    file=open(pos+'mod/'+name+'.mod','w')
    file.write(f'''version="*.*.*"
tags={{
	"Font"
}}
name="{name}"
supported_version="9.9.9"
path="{pos}mod/{name}"''')
    file=open(pos+'mod/'+name+'/descriptor.mod','w')
    file.write(f'''version="*.*.*"
tags={{
	"Font"
}}
name="{name}"
supported_version="9.9.9"
path="{pos}mod/{name}"
picture="thumbnail.png"''')
def insertSQL(name,Default=1,NewAddress=""):    
    conn = sqlite3.connect(pos+'launcher-v2.sqlite')
    c = conn.cursor()
    #name = "ECI Local"
    ModAddress="mod/"+name+".mod"
    RandomID='''0e65a352-015d-478a-b08a-'''+str(random.randint(100000000000,900000000000))
    if Default:
        FileAddress="C:\\Users\\"+user+"\\Documents\\Paradox Interactive\\Stellaris\\mod\\"+name
    else:
        FileAddress=NewAddress+"\\"+name
    
    c.execute(f'''INSERT INTO mods (id,pdxId,steamId,gameRegistryId,name,displayName,descriptionDeprecated,thumbnailUrl,thumbnailPath,version,tags,requiredVersion,arch,os,repositoryPath,dirPath,archivePath,status,source,cause,timeUpdated,isNew,createdDate,subscribedDate,size,metadataId,remotePdxId,remoteSteamId,metadataVersion,isMetadataApplied,metadataStatus,metadataGameId)    VALUES ("{RandomID}",NULL,NULL,"{ModAddress}",NULL,"{name}",NULL,NULL,NULL,"*.*.*",NULL,"3.7.4",NULL,NULL,NULL,"{FileAddress}",NULL,"ready_to_play","local","",NULL,1,1683392067,NULL,69,NULL,NULL,NULL,NULL,0,"not_applied",NULL )''')          

    conn.commit()
    print ("SQL Inserted")
    conn.close()

def zipExtract(Filename,name,Default=1,NewAddress=''):

    if Default:
        save_path = pos+'mod/'+name+'/'
    else:
        save_path=NewAddress+'/'+name
    file=zipfile.ZipFile(Filename)
    file.extractall(save_path)
    file.close()
def run_program():
    filename = entry_filename.get()
    name = entry_name.get()
    
    insertSQL(name)
    zipExtract(filename,name)
    CreateMod(pos, name)

user = getpass.getuser()
pos = "C:/Users/" + user + "/Documents/Paradox Interactive/Stellaris/"
root = tk.Tk()
root.title("Mod Creator")
root.geometry("400x300")

label_filename = tk.Label(root, text="Select a MOD File(zip):")
label_filename.pack()

entry_filename = tk.Entry(root)
entry_filename.pack()

button_browse = tk.Button(root, text="Browse", command=lambda: entry_filename.insert(tk.END, filedialog.askopenfilename()))
button_browse.pack()

label_name = tk.Label(root, text="MOD name:")
label_name.pack()

entry_name = tk.Entry(root)
entry_name.pack()

output_label = tk.Label(root, text="")
output_label.pack()

def run_program():
    filename = entry_filename.get()
    name = entry_name.get()
    
    if filename and name:
        insertSQL(name)
        zipExtract(filename, name)
        CreateMod(pos, name)
        output_label.config(text="Mod created successfully!")
    else:
        output_label.config(text="Please enter both filename and MOD name.")

button_run = tk.Button(root, text="CREATE", command=run_program)
button_run.pack()

root.mainloop()





    
    

#利用Tkinter生成一个GUI界面，输入框包括：zipextract所用的文件名、insertSQL所用的name名