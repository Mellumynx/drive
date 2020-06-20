
import random
import jwt
import os
from flask import Flask, request, jsonify, render_template, url_for, flash, send_from_directory

import mysql.connector
from mysql.connector import Error
from datetime import datetime

from werkzeug.utils import secure_filename

import socket

# key for token
key = 'secret'

# ?
app = Flask(__name__)


# route '/' 
@app.route('/')
def hello_world():
    return 'Hello World!'

# route '/register' methods include POST'
@app.route('/register', methods=['POST'])
def register():
    # initialize variables
    result = ""
    status = "ERROR"

    if request.method == "POST":
        # acquire initial user inputs 
        requestJson = request.json
        username = requestJson['Username']
        password = requestJson['Password']
        confirmation = requestJson['Confirm']

        # connect to database "drive"
        cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
        cursor = cnx.cursor()
        # sql statement, select all users 
        query = "SELECT * FROM users;"
        cursor.execute(query)
        
        for (_, u, p, _,_,_, _) in cursor: 
            """
            run the for loop to check whether the new registered username has been in the database or not: 
                if username input corresponds with correct password -> account exist 
                if username input doesn't correspond with correct password -> username has been taken
            """
            if u == username:
                if p == password: 
                    result = "Account already exist."
                    return jsonify(
                        result = result,
                        status = status
                    )
                else: 
                    result = "Username has been taken."
                    return jsonify(
                        result = result,
                        status = status
                    )
        # if username is new, check whether the password string matches the confirmation string.
        if password == confirmation: 
            # if it does, sql statement (add new user)
            add_Data = "INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');"
            cursor.execute(add_Data)
            result = "Succesfully registered"
            status = "OK"
            
        else:
            # if not, return a statement 
            result = "Password does not match"

        # close connection with database    
        cnx.commit()    
        cursor.close()
        cnx.close()

    # return final statement
    return jsonify(
        result = result,
        status = status
    )

# route '/signin' methods include POST
@app.route('/signin', methods=['POST'])
def signin():
    # initialize variables
    result = "Fail"
    token = ""
    tokenList = []

    # acquire user signin inputs 
    requestJson = request.json
    username = requestJson['Username']
    password = requestJson['Password']

    if request.method == "POST":
        # connect to database "drive"
        cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
        cursor = cnx.cursor() 
        # sql statement select specific user in database
        query = "SELECT * FROM users WHERE username = '" + username + "' ;"
        cursor.execute(query)
        
        # string a current datetime object
        now = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")

        # for loop, check every user whether input password ?
        for (_, u, p, t,_, _, tl) in cursor: 
            if p == password: 
                #sql, append token to tokenlist everytime assigned
                encoded = jwt.encode({"username": username, "timestamp": now}, key, algorithm='HS256')
                
                # set empty token list
                tlt = tl
                if not tlt: 
                    tlt = ""

                # sql statement, add new token to tokenlist
                setToken = "UPDATE users SET tokenList = '" + tlt + ";" + encoded + "' WHERE username = '" + u + "';"
                cursor.execute(setToken) 

                # commit sql statement
                cnx.commit()
                result = "Success"
                break

        # close connection with database   
        cursor.close()
        cnx.close()

    # return final statement
    return jsonify(
        token = token,
        status = result
    )

# set remote folder
UPLOAD_FOLDER = '/Users/apple/Desktop/drive_root_dir/'
# allowed file types
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# route '/upload' methods include POST
@app.route('/upload', methods=['GET', 'POST'])
def upload(): 
    # initialize variables
    status = "ERROR"

    # Authorization (token) ?
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]

    # connect to database "drive"
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    # use token for every functions
    query = "SELECT username FROM users WHERE INSTR(tokenList, '" + token + "');"
    cursor.execute(query)
    
    # check if there is only one user 
    count = 0 
    username = ""
    for u in cursor: 
        count = count + 1
        username = u[0]
    if count < 1:
        return jsonify(
            result = "No username found",
            status = status
        )
    elif count > 1: 
        return jsonify(
            result = "More than 1 user found.",
            status = status
        )

    if request.method == "POST":
        # if file does not exist -> "no files present"
        if 'file' not in request.files:
            return jsonify(
                result = "No files present",
                status = status
            )
        
        # if empty filename, -> "empty filename"
        file = request.files['file']
        if file.filename == '':
            return jsonify(
                result = "Empty filename",
                status = status
            )
        
        # if file exist
        if file: 
            # each person needs each own directory 
            usernamedir = os.path.join(UPLOAD_FOLDER, username)
            # if file directory does not exist, create such directory using username
            if not os.path.isdir(usernamedir):
                os.makedirs(usernamedir)
            
            # upload file
            filename = secure_filename(file.filename)
            file_path = os.path.join(usernamedir, filename)
            file.save(file_path)
            
            status = "OK"
            return jsonify(
                result = "File saved successfully.",
                status = status
            )

    return jsonify(
        status = status
    )

# route '/getAllFiles' methods include GET
@app.route('/getAllFiles', methods=['GET'])
def getAllFiles():
    # initialize variables
    status = "ERROR"
    file_list = []

     # Authorization (token)
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]

    # connect to database "drive"
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    # use token for every functions
    query = "SELECT username FROM users WHERE INSTR(tokenList, '" + token + "');"
    cursor.execute(query)

    # check if there is only one user 
    count = 0 
    username = ""
    for u in cursor: 
        print(u)
        count = count + 1
        username = u[0]
    if count < 1:
        return jsonify(
            result = "No username found",
            status = status
        )
    elif count > 1: 
        return jsonify(
            result = "More than 1 user found.",
            status = status
        )

    # Return all files from given directory
    if request.method == "GET":
        # select directory
        usernamedir = os.path.join(UPLOAD_FOLDER, username)
        # for loop to get all files, and if file name starts with '.' ignore it
        for filename in os.listdir(usernamedir):
            if filename[0] == '.':
                continue
            mtime = os.path.getmtime(os.path.join(usernamedir,filename))
            file_list.append({"filename": filename, "mtime": mtime})
    
    status = "OK"
    return jsonify(
        result = file_list,
        status = status
    )

# route '/download' methods include GET
@app.route('/download', methods=['GET', 'POST'])
def download(): 
    # initialize variables 
    status = "ERROR"

    # Authorization (token)
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]

    # connect to database "drive"
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    # use token for every functions
    query = "SELECT username FROM users WHERE INSTR(tokenList, '" + token + "');"
    cursor.execute(query)

    # check if there is only one user 
    count = 0 
    username = ""
    for u in cursor: 
        count = count + 1
        username = u[0]
    if count < 1:
        return jsonify(
            result = "No username found",
            status = status
        )
    elif count > 1: 
        return jsonify(
            result = "More than 1 user found.",
            status = status
        )

    # connect to client, request filename
    filename = request.args.get("filename")
    if not filename or len(filename) == 0: 
        return jsonify(
            result = "Filename is not specified.",
            status = status
        )

    # Use directory to download
    if request.method == "GET":
        path = os.path.join(UPLOAD_FOLDER, username)
        return send_from_directory(path, filename, as_attachment=True)

    
    return jsonify(
        status = status
    )



@app.route('/delete', methods=['GET', 'POST'])
def delete(): 
    # Authorization (token)
    status = "ERROR"
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]

    # get username
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    query = "SELECT username FROM users WHERE INSTR(tokenList, '" + token + "');"
    cursor.execute(query)

    count = 0 
    username = ""
    for u in cursor: 
        count = count + 1
        username = u[0]
    if count < 1:
        return jsonify(
            result = "No username found",
            status = status
        )
    elif count > 1: 
        return jsonify(
            result = "More than 1 user found.",
            status = status
        )

    requestForm = request.form
    if "filename" not in requestForm:
        return jsonify(
            result = "Filename not found.",
            status = status
        )

    filename = requestForm['filename']
    if request.method == "POST":
        remove_file = os.path.join(UPLOAD_FOLDER, username, filename)
        path = os.remove(remove_file)
        return jsonify(
            result = "File removed succesfully",
            status = status
        )
    
    return jsonify(
        status = status
    )


if __name__ == '__name__':
    app.run(debug=True)



