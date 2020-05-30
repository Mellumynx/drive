from flask import Flask, request, jsonify, render_template
import random
import jwt
key = 'secret'


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user', methods=['GET', 'POST'])
def register():
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
        if password == confirmation:
            encoded = jwt.encode({'some_x': 'payload_y'}, key, algorithm='HS256')
            #store token (encoded)
            return "Success"
            """
            return jsonify({
                "User": username,
                "Password": password
            }) #ACID database (consistency)
            """
        else: 
            return "Password does not match!"
        
# Setup a mysql DB, 
#return "success" / "Fail (reason)"
# upload to github
# save token to DB


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        # if(requestJson['Username'] == username and requestJson['Password'] == password):
            token = random.randint(100, 999)
            return str(token)



"""
@app.route('')
def upload(): 
"""


if __name__ == '__name__':
    app.run(debug=True)

