#!/usr/bin/env python

#a17A1m1_


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
    """Работа с DB::
    
        DB.GET('sql code') `Получение данных`
        ::
        
        DB.POST('sql code') `Отправка данных`
    """
    def GET(self):#(host="host", user="username",   password ="pwd", database="db")
        connection = pymysql.connect(host="37.140.192.16", user='u0689235_wwb_21', password='WWB_2021', database='u0689235_wwb_2021', charset="utf8")
        cursor = connection.cursor()
        cursor.execute(self)
        OTV = cursor.fetchall()
        return(OTV)
        
    def POST(self):
        connection = pymysql.connect(host="37.140.192.16", user='u0689235_wwb_21', password='WWB_2021', database='u0689235_wwb_2021', charset="utf8")
        cursor = connection.cursor()  
        cursor.execute(self) 
        connection.commit()
        return('True')




@application.route('/', methods=['GET', 'POST'])
def index():
    
    return(str(DB.GET('select * from skills')))

@application.route('/API/getSkills', methods=['GET', 'POST'])
def API_getSkills():
    if request.method == "GET":
        req = {}
        # Na =  DB.GET('SELECT groupSkills.Name, groupSkills.id, skills.name FROM `groupSkills`, `skills` WHERE groupSkills.id = skills.fromGroup')
        sqlReq = DB.GET('SELECT groupSkills.Name, groupSkills.id, skills.name, skills.id FROM `groupSkills`, `skills` WHERE groupSkills.id = skills.fromGroup')
        print(sqlReq)
        
        for el in sqlReq:
            print(el)
            try:
                print(req[el[1]])
            except:
                req[el[1]] = {
                    'name':None,
                    'objects':{}
                }
            req[el[1]]['name'] = el[0]
            print('s',req)
            req[el[1]]['objects'][len(req[el[1]]['objects'])] = {'id':el[3], 'name':el[2]}
            
            
        return (req)






@application.errorhandler(404)
def page_not_found(e):
    return ("errors") #('404.html')


if __name__=="__main__":
    application.run(host='localhost', debug=True, port=8001, threaded=True)