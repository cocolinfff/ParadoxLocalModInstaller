import sqlite3
import random
import getpass

def CreateMod(pos,name):
    file=open(pos+'mod/'+name+'.mod','w')
    file.write(f'''version="*.*.*"
tags={{
	"Font"
}}
name="{name}"
supported_version="3.7.4"
path="{pos}mod/{name}"''')
    file=open(pos+'mod/'+name+'/descriptor.mod','w')
    file.write(f'''version="*.*.*"
tags={{
	"Font"
}}
name="{name}"
supported_version="3.7.4"
path="{pos}mod/{name}"
picture="thumbnail.png"''')
    
    
    
user=getpass.getuser()
pos="C:/Users/"+user+"/Documents/Paradox Interactive/Stellaris/"
conn = sqlite3.connect(pos+'launcher-v2.sqlite')
c = conn.cursor()
name = "ECI Local"
ModAddress="mod/"+name+".mod"
RandomID='''0e65a352-015d-478a-b08a-'''+str(random.randint(100000000000,900000000000))
FileAddress="C:\\Users\\"+user+"\\Documents\\Paradox Interactive\\Stellaris\\mod\\"+name
c.execute(f'''INSERT INTO mods (id,pdxId,steamId,gameRegistryId,name,displayName,descriptionDeprecated,thumbnailUrl,thumbnailPath,version,tags,requiredVersion,arch,os,repositoryPath,dirPath,archivePath,status,source,cause,timeUpdated,isNew,createdDate,subscribedDate,size,metadataId,remotePdxId,remoteSteamId,metadataVersion,isMetadataApplied,metadataStatus,metadataGameId)    VALUES ("{RandomID}",NULL,NULL,"{ModAddress}",NULL,"{name}",NULL,NULL,NULL,"*.*.*",NULL,"3.7.4",NULL,NULL,NULL,"{FileAddress}",NULL,"ready_to_play","local","",NULL,1,1683392067,NULL,69,NULL,NULL,NULL,NULL,0,"not_applied",NULL )''')          
          
conn.commit()
print ("success")
conn.close()



import zipfile
import os
save_path = pos+'mod/'+name+'/'

file=zipfile.ZipFile("master.zip")
file.extractall(save_path)
file.close()
CreateMod(pos,name)