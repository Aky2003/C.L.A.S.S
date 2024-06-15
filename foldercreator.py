import os
import shutil
import zipfoldercreate
def createfolder(name):
    newpath = r"C:\Users\aksha\OneDrive\Desktop\c2"
    folder_name = "Folder of " + f'{name}'
    full_path = os.path.join(newpath, folder_name)
    os.makedirs(full_path, exist_ok=True)
    htmlname = "CASEOF_"+name+".html"
    # print(htmlname)
    htmlpath = os.path.join(newpath, htmlname)
    imagepath=r"C:\Users\aksha\OneDrive\Desktop\c2\uploads"
    shutil.move(imagepath,full_path)
    shutil.move(htmlpath, full_path)
    # print(full_path)
    zipfoldercreate.send_email_with_folder(full_path,folder_name,name)


