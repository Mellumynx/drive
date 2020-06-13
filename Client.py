#!/usr/bin/python
import time

import requests


def main():
    while(True):
        time.sleep(5)
        sync()

def sync():
    URL = "http://127.0.0.1:5000/getAllFiles"
    headers = {'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRva2VuIiwidGltZXN0YW1wIjoiMTItSnVuLTIwMjAgKDE3OjMwOjI2Ljc5MjE2MikifQ.zablyO9VkZg0fFRNImGsgH1sJiccn4DKlNsFIh9DXAk'}
    r = requests.get(url = URL, headers=headers)
    # class time: 1. comparison (if statement) 
    # how to get current modifed time by file 

    data = r.json()
    print(data)

    
        
    # use token - > get all files
    # compare with local files
    # if only one file exist, use file
    # if not (time same) = no change
    #        (time different) = timestamp (new) 

    """
    1. first use : cloud no file / local has file = current api (check)
    2. second + use : update existing file = upload every 5 mins (no) ??
    3. new local client : cloud has file / new local no file (no)
    4. different client communication (no)

    Timestamp: upload, edited ??
    """

        # timestamp (pacific)
        # support multiple token = username + ip

    # note to self: (api action time limit: 5 min when active) = token list
        # check user (activation)  ~ different ip / remove existing
        # get full list from server
        # compare list (to local)
            # if equal
                # (check)
            # elif (no such document) docuemnt id (new variable)
                # upload/download accorindly
            # else 
                # check "modified time" (new variable) = upload/download accordingly 
                # if local modified time < server modified time: download & replace new version
                # if server modifed < local modifed time: upload 
        




if __name__ == "__main__":
     main()