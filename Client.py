#!/usr/bin/python
import time
import os
import requests
import shutil
import tempfile
import difflib
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True)
    parser.add_argument('--local_dir', required=True)
    args = parser.parse_args()
    print(args.token)
    print(args.local_dir)
    while(True):
        time.sleep(2)
        sync(args.token, args.local_dir)

def run_cmp(filename1, filename2):
    cmd = 'cmp --verbose %s %s'%(filename1, filename2)
    stream = os.popen(cmd)
    output = stream.read()
    return len(output)


def sync(token, dir):
    # remote, 
    URL = "http://127.0.0.1:5000/getAllFiles" 
    headers = {'Authorization' : 'Bearer ' + token}
    # use url, token to get request.
    r = requests.get(url = URL, headers=headers)
    data = r.json()

    # if there is no result -> "no result found", else store results in file_List_Remote
    if "result" not in data: 
        return "No result found"
    file_List_Remote = data["result"]

    # local
    local_Folder = dir
    file_List_Local = []
    for filename in os.listdir(local_Folder):
        # ignore all files start with '.'
        if filename[0] == '.':
            continue
        # get modified time for each file
        mtime = os.path.getmtime(os.path.join(local_Folder,filename))
        # add to file_List_Local
        file_List_Local.append({"filename": filename, "mtime": mtime})

    # compare
    intersectFiles = []
    # nested for loop, select files in both file_List_Remote and file_List_Local
    for localfile in file_List_Local: 
        for remotefile in file_List_Remote: 
            if localfile["filename"] == remotefile["filename"]:
                intersectFiles.append(localfile["filename"])
    
    # upload/download
    filesToUpload = []
    filesToDownload = []
    for localfile in file_List_Local: 
        if localfile["filename"] not in intersectFiles:
            filesToUpload.append(localfile["filename"])

    for remotefile in file_List_Remote:
        if remotefile["filename"] not in intersectFiles:
            filesToDownload.append(remotefile["filename"])
    
    # for every file, get modified time for both local and remote 
    for f in intersectFiles:
        local_time = 0
        remote_time = 0
        for localFileObject in file_List_Local: 
            if localFileObject["filename"] == f: 
                local_time = localFileObject["mtime"]
                break

        for remoteFileObject in file_List_Remote: 
            if remoteFileObject["filename"] == f: 
                remote_time = remoteFileObject["mtime"]
                break
        
        # make a comparison whether to upload/download
        if local_time > remote_time:
            filesToUpload.append(f)

        elif local_time < remote_time:
            filesToDownload.append(f) 

   
    #print("Files to upload: " + ','.join(filesToUpload))
    #print("Files to download: " + ','.join(filesToDownload))


    upload = "http://127.0.0.1:5000/upload"
    for actionFile in filesToUpload: 
        # open (file)
        with open(os.path.join(local_Folder, actionFile), 'rb') as f:
            u = requests.post(upload, headers = headers, files = {"file": f})
            print("Upload " + actionFile + ':' + str(u.content))
    
    download = "http://127.0.0.1:5000/download"
    for actionFile in filesToDownload: 
        d = requests.get(download, headers = headers, params = {"filename": actionFile})
        content = d.content

        with tempfile.TemporaryDirectory() as tmpdirname:
            #print('created temporary directory', tmpdirname)
        
            with open(os.path.join(tmpdirname, actionFile), 'wb') as location:
                location.write(content)
                #print("Downloaded " + filename)

            # print("diffbyte:" + str(run_cmp(os.path.join(local_Folder, actionFile), os.path.join(tmpdirname, actionFile))))

            if not os.path.isfile(os.path.join(local_Folder, actionFile)) or run_cmp(os.path.join(local_Folder, actionFile), os.path.join(tmpdirname, actionFile)) != 0: 
                shutil.copyfile(os.path.join(tmpdirname, actionFile), os.path.join(local_Folder, actionFile))
                print("localfile updated: " + actionFile)

if __name__ == "__main__":
     main()