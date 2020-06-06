from flask import Flask, request, jsonify, render_template
import random
import jwt

import mysql.connector
from mysql.connector import Error


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
        
        for (_, u, p, _,_, t) in cursor: 
            print(u)
            print(p)
            if p == password: 
                encoded = jwt.encode({'some_x': 'payload_y'}, key, algorithm='HS256')
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




@app.route('/upload', methods=['GET', 'POST'])
def upload(): 
    requestFile = request.files
    if 




if __name__ == '__name__':
    app.run(debug=True)

