#!/usr/bin/env python
from flask import Flask, render_template, request, session, Response, make_response, redirect, jsonify
from flask_cors import CORS
import datetime
import json
import uuid
import hashlib
import sqlite3
import pymysql
import time
import string
import random
application = Flask(__name__)

CORS(application)

class DB():
    def GET(self):#(host="host", user="username",   password ="pwd", database="db")
        connection = pymysql.connect(host="75.119.142.143", user='barsuks', password='M90vHrM1HQIjcRxA', database='pars', charset="utf8")
        cursor = connection.cursor()
        cursor.execute(self)
        OTV = cursor.fetchall()
        return(OTV)
        
    def POST(self):
        connection = pymysql.connect(host="75.119.142.143", user='barsuks', password='M90vHrM1HQIjcRxA', database='pars', charset="utf8")
        cursor = connection.cursor()  
        cursor.execute(self) 
        connection.commit()
        return('True')

@application.route('/', methods=['GET', 'POST'])
def index():
    return('ss')

@application.route('/', methods=['GET', 'POST'])
def API_GGG(GetElement):
    pass

@application.errorhandler(404)
def page_not_found(e):
    return ("errors") #('404.html')


if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True, port=8001, threaded=True)