#!/usr/bin/env python

#a17A1m1_


from flask import Flask, render_template, request, session, Response, make_response, redirect, jsonify
from flask_cors import CORS
import traceback 
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


    def Check_user_in_db(self, login, password):
        connection = pymysql.connect(host="37.140.192.16", user='u0689235_wwb_21', password='WWB_2021', database='u0689235_wwb_2021', charset="utf8")
        cursor = connection.cursor()
        cursor.execute(f'select password, role, id_user id from authData where login = "{login}"')
        OTV = cursor.fetchall()
        error = 0
        ids = 0
        try:
            if(str(OTV[0][0]) == password):
                error = 0
                ids = OTV[0][2]
            else:
                error = 2
        except:
            error = 1
        return(error, ids, OTV[0][1])



@application.route('/', methods=['GET', 'POST'])
def index():
    return('API from Sochi :}')

@application.route('/API/getSkills', methods=['GET', 'POST'])
def API_getSkills():
    try:
        TN = str(time.time())
        TN = TN[:TN.find('.')]
        TM = str(request.form['timeN'])[0:-3]
        RZ = (int(TN) - int(TM))
        if(RZ <= 10 and RZ >= -5):
        
            if request.method == "GET":
                req = {}
                # Na =  DB.GET('SELECT groupSkills.Name, groupSkills.id, skills.name FROM `groupSkills`, `skills` WHERE groupSkills.id = skills.fromGroup')
                sqlReq = DB.GET('SELECT groupSkills.Name, groupSkills.id, skills.name, skills.id FROM `groupSkills`, `skills` WHERE groupSkills.id = skills.fromGroup')
                # print(sqlReq)
                
                for el in sqlReq:
                    # print(el)
                    try:
                        a = (req[el[1]])
                    except:
                        req[el[1]] = {
                            'name':None,
                            'objects':{}
                        }
                    req[el[1]]['name'] = el[0]
                    # print('s',req)
                    req[el[1]]['objects'][len(req[el[1]]['objects'])] = {'id':el[3], 'name':el[2]}
                    
                    
                return (req)
            else:
                return('Пока что GET')

        else:
            return('Время истекло')
    except:
        return('API not found') 

@application.route('/API/getlocation', methods=['GET', 'POST'])
def API_getlocation():
    try:
        print(request.form)
        TN = str(time.time())
        TN = TN[:TN.find('.')]
        TM = str(request.form['timeN'])[0:-3]
        RZ = (int(TN) - int(TM))
        if(RZ <= 10 and RZ >= -5):

            req = {}
            print(req)
            # Na =  DB.GET('SELECT groupSkills.Name, groupSkills.id, skills.name FROM `groupSkills`, `skills` WHERE groupSkills.id = skills.fromGroup')
            sqlReq = DB.GET('SELECT * FROM location')
                            
            print(sqlReq)
            
            for el in range(0, len(sqlReq)):
                try:
                req[el] = {
                        'id':sqlReq[el][0],
                        'title': str(sqlReq[el][1])
                    }
                except:
                    pass   
            return (req)
    except:
        return('API critical error')  

@application.route('/API/checkauth', methods=['GET', 'POST'])
def checkauth():
    try:
        returnValue = {
            'method': None
            }
        TN = str(time.time())
        TN = TN[:TN.find('.')]
        TM = str(request.form['timeN'])[0:-3]
        RZ = (int(TN) - int(TM))
        if(RZ <= 10 and RZ >= -5):
            print(request.form)
            rt = {
                'ErrorP': False,
                'ErrorL': False,
                'role': None,
                'id_u':None
                }
            try:
                codeE, id_u, role = DB.Check_user_in_db(None, request.form['login'], request.form['password'])
                print(codeE, id_u, role)
                if codeE == 1:
                    rt['ErrorL'] = True
                    rt['ErrorP'] = True
            
                if(codeE == 2):
                    rt['ErrorP'] = True
                
                if(codeE == 0):
                    rt['role'] = role
                    rt['id_u'] = id_u
                    
                return(rt, 200)
            except:
                return('Неверные данные', 200)
        else:
            return('Время истекло')
    except:
        return('API critical error')  

@application.route('/API/createaccount/<role>', methods=['GET', 'POST'])
def createaccount(role):
    try:
        TN = str(time.time())
        TN = TN[:TN.find('.')]
        TM = str(request.form['timeN'])[0:-3]
        RZ = (int(TN) - int(TM))
        if(RZ <= 10 and RZ >= -5):
            #role
            # 1 - Студент
            # 2 - Работодатель
            # 3 - Учебное Заведение 
            if(type(int(role)) == int):
            
                if(int(role) == 1):
                    req = request.form
                    text = (f'select login from authData where login = "{req["login"]}"')
                    print(req)
                    mails = DB.GET(text)
                    print('create', req,'\n',mails,'\n')
                    error = {
                        'loginE':None,
                        'status': None
                    }
                    
                    try:
                        if(mails[0][0] == req["login"]):error['loginE'] = True; error['status'] = 'login занят'
                    except:
                        pass
                    
                    print(error)
                    if(error['loginE'] == None):
                        print('Создание аккаунта студента' ,req)
                        try:
                            text = (f"""
                                INSERT INTO `student`(`id`, `name`, `last_name`, `faculty`, `from_educational`, `about`, `email`, `phone`)
                                VALUES (Null, "{req['name']}", "{req['last_name']}", "{req['faculty']}", "{req['educational']}", "", "", "")
                                """)
                            DB.POST(text)
                            maxC = DB.GET('SELECT id FROM student ORDER BY id DESC LIMIT 1')
                            print(maxC[0][0])
                            text = (f"""
                                INSERT INTO `authData`(`id`, `id_user`, `login`, `password`, `role`) 
                                VALUES (null, {maxC[0][0]}, "{req["login"]}", "{req["password"]}", 1)
                                """)
                            DB.POST(text)
                            text = (f"""
                                INSERT INTO `talants`(`id`, `from_user`, `id_skill`) 
                                VALUES (null, {maxC[0][0]}, '0')
                                """)
                            DB.POST(text)
                            error['status'] = 'True'
                            return(error)
                        except:
                            return('API error <не верное колличество данных или они не корректны>')
                        
                        
                    return(error, 200)
            
            
                elif(int(role) == 2):
                    req = request.form
                    text = (f'select login from authData where login = "{req["login"]}"')
                    print(req)
                    mails = DB.GET(text)
                    print('create', req,'\n',mails,'\n')
                    error = {
                        'loginE':None,
                        'status': None
                    }
                    
                    try:
                        if(mails[0][0] == req["login"]):error['loginE'] = True; error['status'] = 'login занят'
                    except:
                        pass
                    
                    print(error)
                    if(error['loginE'] == None):
                        print('Создание аккаунта работодателя' ,req)
                        try:
                            text = (f"""
                                INSERT INTO `employer`(`id`, `company_name`, `direction`, `count_staff`) 
                                VALUES (null, "{req['company_name']}", "{req['direction']}", {req['count_staff']})
                                """)
                            DB.POST(text)
                            maxC = DB.GET('SELECT id FROM employer ORDER BY id DESC LIMIT 1')
                            print(maxC[0][0])
                            text = (f"""
                                INSERT INTO `authData`(`id`, `id_user`, `login`, `password`, `role`) 
                                VALUES (null, {maxC[0][0]}, "{req["login"]}", "{req["password"]}", 2)
                                """)
                            DB.POST(text)
                            error['status'] = 'True'
                            return(error)
                        except:
                            return('API error <не верное колличество данных или они не корректны>')
                
                    return(error, 200)
                    
                    
                elif(int(role) == 3):
                    req = request.form
                    text = (f'select login from authData where login = "{req["login"]}"')
                    print(req)
                    mails = DB.GET(text)
                    print('create', req,'\n',mails,'\n')
                    error = {
                        'loginE':None,
                        'status': None
                    }
                    
                    try:
                        if(mails[0][0] == req["login"]):error['loginE'] = True; error['status'] = 'login занят'
                    except:
                        pass
                    
                    print(error)
                    if(error['loginE'] == None):
                        print('Создание аккаунта образованию' ,req)
                        try:
                            text = (f"""
                                INSERT INTO `establishment`(`id`, `location`, `title`, `type`) 
                                VALUES (null, "{req['location']}", "{req['title']}", "{req['type']}")
                                """)
                            DB.POST(text)
                            maxC = DB.GET('SELECT id FROM establishment ORDER BY id DESC LIMIT 1')
                            print(maxC[0][0])
                            text = (f"""
                                INSERT INTO `authData`(`id`, `id_user`, `login`, `password`, `role`) 
                                VALUES (null, {maxC[0][0]}, "{req["login"]}", "{req["password"]}", 3)
                                """)
                            DB.POST(text)
                            error['status'] = 'True'
                            return(error)
                        except:
                            return('API error <не верное колличество данных или они не корректны>')
                
                    return(error, 200)
                    
            
            
            else:
                return('API not found', 404)
        else:
            pass
        return('pass')        
    except:
        return('API critical error')  
    
@application.route('/API/findastudent', methods=['GET', 'POST'])
def findastudent():
    try:
        print(request.form)
        TN = str(time.time())
        TN = TN[:TN.find('.')]
        TM = str(request.form['timeN'])[0:-3]
        RZ = (int(TN) - int(TM))
        if(RZ <= 10 and RZ >= -5):
            req = request.form
            
            skillsToDB = str(req['skills']).replace(']','').replace('[','')
            massSkills = skillsToDB.split(',')
            print(skillsToDB, massSkills)
            
            a = DB.GET(f'SELECT zakaz_id FROM employer where id = {req["from_employer"]}')
            print(a)
            try:
                zakazId = str(a[0][0])
                if(zakazId == 'None' or int(zakazId) == 0):
                    print('пп')
                    DB.POST(f"""INSERT INTO zakaz (id, from_employer, need_skills, info, location) 
                            VALUES (null, "{req['from_employer']}", "{skillsToDB}", {req['info']}, "{req['location']}")""")
                    
                    maxC = DB.GET('SELECT id FROM zakaz ORDER BY id DESC LIMIT 1')
                    
                    DB.POST(f'UPDATE employer SET zakaz_id = {maxC[0][0]}')
                    
                    establishment_in_location = DB.GET(f"""SELECT id FROM establishment WHERE location = {req['location']} """)
                    Texqmain = 'INSERT INTO malling_establishment (id, to_establishment, from_employer, id_zakaz, status) VALUES'
                    for el in establishment_in_location:
                        tex = str(f' (null, {el[0]}, {req["from_employer"]}, {maxC[0][0]}, "not viewed"),')
                        Texqmain += (tex)
                    a = str(Texqmain)[:-1]
                    print(a)
                    DB.POST(a)
                    
                    
                else:
                    return('Уже есть активный поиск студента')
            except:
                print(traceback.format_exc())
                return('ошибка, нет такого пользователя')
        
        return('Поиска студента')
    except:
        return('API critical error')

@application.route('/API/whenconnecting', methods=['GET', 'POST'])
def whenconnecting():
    try:
        print(request.form)
        TN = str(time.time())
        TN = TN[:TN.find('.')]
        TM = str(request.form['timeN'])[0:-3]
        RZ = (int(TN) - int(TM))
        if(RZ <= 10 and RZ >= -5):
            try:
                role = DB.GET(f'SELECT role FROM authData where id_user = {request.form["who_is_connect"]}')[0][0]
                print(role)
                if(int(role) == 3):   
                    texq = {
                        'text': None,
                        'sysText':None
                    }
                    
                    try:
                        # r = DB.GET(f"""SELECT * FROM malling_establishment where to_establishment = {request.form['who_is_connect']} and status = "not viewed" """)
                        # DB.POST(F"""UPDATE malling_establishment SET status = 'viewed' where id = {r[0][0]}""") # поставить в то место где открывается страница заказов
                        otv = DB.GET(f"""SELECT from_employer, id_zakaz FROM malling_establishment where to_establishment = {request.form['who_is_connect']} and status = "not viewed" """)
                        c_id = ''
                        for el in otv:
                            c_id += str(el[0]) + ',' 
                        c_id = c_id[:-1]
                        otvs = DB.GET(f"""SELECT company_name FROM employer where employer.id in ({c_id})""")
                        if(len(otv) < 1):
                            texq['text'] = f"""Компания `{otvs[0][0]}` оставила заявку посетите личный кабинет"""
                            texq['sysText'] = 'Уведомления есть'
                        else:
                            texq['text'] = f"""Компании ({len(otv)}) оставили заявку посетите личный кабинет"""
                            texq['sysText'] = 'Уведомления есть'
                        return(texq, 200)
                    except:
                        texq['sysText'] = 'Нет уведомлений'
                        return(texq, 200)
                
                elif(int(role) == 2):
                    print('role', role)
                    texq = {
                        'text': None,
                        'sysText':None}
                    try:
                        q = DB.GET(f'SELECT * FROM establishment_base_return where from_employer = {request.form["who_is_connect"]} and status = "sended" ')
                        if(len(q) > 0):
                            texq['text'] = f"""Учебных заведений ({len(q)}) отправили отчёт. Посетите личный кабинет"""
                            texq['sysText'] = 'Уведомления есть'
                        else: texq['sysText'] = 'Нет уведомлений'
                            
                    except:
                        pass
                    return(texq, 200)
                    
                elif(int(role) == 1):
                    texq = {
                        'text': None,
                        'sysText':None
                    }
                    try:
                        sta = DB.GET(f'select zakaz_id from mailing where to_user = {request.form["who_is_connect"]}')
                        print(sta)
                        if(len(sta) > 0):
                            texq['text'] = f"""Компании ({len(sta)}) ищут стажёров по вашей специальности. Посетите личный кабинет"""
                            texq['sysText'] = 'Уведомления есть'
                        else: texq['sysText'] = 'Нет уведомлений'
                    except:
                        pass

                    return(texq, 200)
                
                else:
                    return('API not working')
            except:
                return('API critical error')
        
        return('API from Sochi :}')
    except:
        return('API critical error')

@application.errorhandler(404)
def page_not_found(e):
    return ("errors") #('404.html')


if __name__=="__main__":
    application.run(host='0.0.0.0', debug=True, port=8001, threaded=True)