from flask import Flask
app = Flask(__name__)

@app.route('/')
#def hello_world():
#    return 'Hello world!'

def register():
    username = input('Enter username: ')
    password = input('Enter password: ')
    confirmation = input('Confirm the password: ')
    if(password == confirmation):
        return 1
    else:
        return 0


def login():
    #username
    #password
    #return token (IP, Time)
    return 0

def upload():
    #token (check valid)
    return 0

def partialUpload():
    #token
    return 0

def delete():
    #token
    return 0

def trash():
    #token
    return 0
