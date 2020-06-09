import random
import jwt
import os
from flask import Flask, request, jsonify, render_template, url_for, flash, send_from_directory

import mysql.connector
from mysql.connector import Error
from datetime import datetime

from werkzeug.utils import secure_filename

key = 'secret'


app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    result = ""
    status = "ERROR"
    if request.method == "GET":
        return jsonify({
            "User": "username",
            "Pwd": "password"
        })
    elif request.method == "POST":
        requestJson = request.json
        username = requestJson['Username']
        password = requestJson['Password']
        confirmation = requestJson['Confirm']

        cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
        cursor = cnx.cursor()
        query = "SELECT * FROM users;"
        cursor.execute(query)
        
        print(password)
        print(confirmation)
        for (_, u, p, _,_,_) in cursor: 
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

        if password == confirmation: 
            """
            #encoded = jwt.encode({'some_x': 'payload_y'}, key, algorithm='HS256')
            # encode difference: encode, key, algorithm, (Update)
            """
            add_Data = "INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "');"
            cursor.execute(add_Data)
            result = "Succesfully registered"
            status = "OK"
            
        else: 
            result = "Password does not match"
            
        cnx.commit()    
        cursor.close()
        cnx.close()

    return jsonify(
        result = result,
        status = status
    )


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    result = "Fail"
    requestJson = request.json
    username = requestJson['Username']
    password = requestJson['Password']
    token = ""
    if request.method == "POST":
        cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
        cursor = cnx.cursor() 
        query = "SELECT * FROM users WHERE username = '" + username + "' ;"
        cursor.execute(query)
        
        now = datetime.now()
        for (_, u, p, t,_, _) in cursor: 
            print(u)
            print(p)
            if p == password: 
                encoded = jwt.encode({"username": username, "timestamp": now}, key, algorithm='HS256')
                sql = "UPDATE users SET token = '" + encoded + "' WHERE username = '" + u + "';"
                print(sql)
                cursor.execute(sql) 
                result = "Success"
                token = encoded
                break

        cursor.close()
        cnx.close()

    return jsonify(
        token = token,
        status = "OK"
    )



# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# UPLOAD = '/Users/apple/Desktop/'
UPLOAD_FOLDER = '/Users/apple/Desktop/drive_root_dir/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""

@app.route('/upload', methods=['GET', 'POST'])
def upload(): 
    # Authorization (token)
    status = "ERROR"
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]
    print(token)

    # Search user
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    query = "SELECT username FROM users WHERE token = '" + token + "';"
    cursor.execute(query)

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

    # Post selected file
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify(
                result = "No files present",
                status = status
            )

        file = request.files['file']
        if file.filename == '':
            return jsonify(
                result = "Empty filename",
                status = status
            )
        if file: # each person needs each own directory 
            usernamedir = os.path.join(UPLOAD_FOLDER, username)
            print(usernamedir)
            if not os.path.isdir(usernamedir):
                os.makedirs(usernamedir)
            
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


@app.route('/getAllFiles', methods=['GET', 'POST'])
def getAllFiles():
    status = "ERROR"
     # Authorization (token)
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]
    print(token)

    # get username
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    query = "SELECT username FROM users WHERE token = '" + token + "';"
    cursor.execute(query)

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
    file_list = []
    if request.method == "GET":
        #json list files
        usernamedir = os.path.join(UPLOAD_FOLDER, username)
        for filename in os.listdir(usernamedir):
            file_list.append(os.path.join(usernamedir, filename))
    
    status = "OK"
    return jsonify(
        result = file_list,
        status = status
    )

@app.route('/download', methods=['GET', 'POST'])
def download(): 
      # Authorization (token)
    status = "ERROR"
    if "Authorization" not in request.headers:
        return jsonify(
            status = status
        )
    token = request.headers["Authorization"][7:]
    print(token)

    # get username
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    query = "SELECT username FROM users WHERE token = '" + token + "';"
    cursor.execute(query)

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

    requestForm = request.form
    # filename = requestJson['filename']
    if "filename" not in requestForm:
        return jsonify(
            result = "Filename not found.",
            status = status
        )
    filename = requestForm['filename']

    print(filename)
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
    print(token)

    # get username
    cnx = mysql.connector.connect(user="frover", password="frover", host="34.67.158.25", database="drive")
    cursor = cnx.cursor() 
    query = "SELECT username FROM users WHERE token = '" + token + "';"
    cursor.execute(query)

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

    requestForm = request.form
    # filename = requestJson['filename']
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



