#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
import re
import requests
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
import traceback
import matplotlib.pyplot as plt #그래프 그리기
import matplotlib               #그래프 그리기
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #그래프
from matplotlib.figure import Figure                            #그래프
import numpy as np

TOKEN = '6039531392:AAGvMkW36gQeXsZ2D8MV6lfBLP6Og81dW-U'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getData():
    mapUrl = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire'
    sumList = []
    mapParams = {'serviceKey' : 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==',
         'Q0' : '서울특별시',
         'pageNo' : '1', 
         'numOfRows' : '100'
         }
    
    mapResponse = requests.get(mapUrl, params=mapParams)
    mapRoot = ET.fromstring(mapResponse.text)

    for item in mapRoot.iter("item"):
        data = str(item.findtext("dutyName")+' / '+item.findtext("dutyAddr")+' / '+item.findtext("dutyTel1"))
        sumList.append(data)
    return sumList

def getGraph(name):
    # 한글깨짐현상 해결(그래프)
    matplotlib.rcParams['font.family'] = 'Malgun Gothic'  

    # 기관ID 가져오기
    base_url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire'
    params = {
        'serviceKey': 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==',
        'QN': name
    }

    response = requests.get(base_url, params=params)
    root = ET.fromstring(response.text)
    duty_id_element = root.find('.//item//hpid')
    
    # duty_id_element가 None일 경우에 대한 처리
    if duty_id_element is not None:
        org_id = duty_id_element.text
    else:
        messagebox.showinfo("오류", "없는 기관입니다.")
        return

    # 응급실, 일반중환자실, 신생아중환자실, 수술실 정보 가져오기
    info_url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytBassInfoInqire'
    info_params = {
        'serviceKey': 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==',
        'HPID': org_id
    }
    info_response = requests.get(info_url, params=info_params)
    info_root = ET.fromstring(info_response.text)
    info_data = []
    for element in info_root.findall('.//item'):
        hperyn_element = element.find('hperyn')
        hpicuyn_element = element.find('hpicuyn')
        hpnicuyn_element = element.find('hpnicuyn')
        hpopyn_element = element.find('hpopyn')

        hperyn = int(hperyn_element.text) if hperyn_element is not None else 0
        hpicuyn = int(hpicuyn_element.text) if hpicuyn_element is not None else 0
        hpnicuyn = int(hpnicuyn_element.text) if hpnicuyn_element is not None else 0
        hpopyn = int(hpopyn_element.text) if hpopyn_element is not None else 0

        s = '이름: ' +name+'\n'+\
            '응급실: '+str(hperyn)+' 개 일반중환자실: '+str(hpicuyn)+'개'+'\n'\
              '신생아중환자실: '+str(hpnicuyn)+'개 수술실: '+str(hpopyn)+'개'
        info_data.append(s)
        return info_data

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(area_param, page_param, num_param):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        res_list = getData(area_param, page_param, num_param)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)