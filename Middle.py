# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import requests
import xml.etree.ElementTree as ET
import tkinter.ttk #notebook사용



class Emergency:
    def mapping(self):
        pass
    def baseData(self,frame,num):       # 기본 정보 추출
        url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytBassInfoInqire'

        params ={'serviceKey' : 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==', 
                 'pageNo' : str(num), 
                 'numOfRows' : '20'
                 }
        
        '''
        self.windowBase = Tk()
        self.windowBase.title("BaseData")
        self.windowBase.geometry('1500x600')
        '''
        if num > 1:
            self.frameBase.destroy()    #num이 1이 아닐때는 지우고 다시출력(수정해야됨)
        self.frameBase = Frame(frame)
        self.frameBase.pack()
        

        response = requests.get(url, params=params)
        print(response.text)
        root = ET.fromstring(response.text)
        Header = ["이름","주소","전화번호"]

        # scrollbar=Scrollbar(self.frameBase)
        # scrollbar.pack(side=RIGHT, fill=Y)

        # self.text = Text(self.frameBase, width=150, height=100,wrap=WORD,yscrollcommand=scrollbar.set)
        # self.text.pack()
        # scrollbar.configure(command=self.text.yview)

        for i, col_name in enumerate(Header):
            label = Label(self.frameBase, text=col_name, font=("Helvetica", 20, "bold"))
            label.grid(row=0, column=i)

        row_count = 1

        for item in root.iter("item"):
            dutyName = item.findtext("dutyName")        # 이름
            dutyAddr = item.findtext("dutyAddr")        # 주소
            dgidIdName = item.findtext("dgidIdName")    # 진료과목
            dutyTel1 = item.findtext("dutyTel1")
            

            data = [dutyName, dutyAddr, dutyTel1]
            for i, value in enumerate(data):
                label = Label(self.frameBase, text=value, font=("Helvetica", 9))
                label.grid(row=row_count, column=i)   
            row_count += 1     
    
    def subData(self,frame,name):
        self.url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire' #응급의료기관 목록조회

        self.params ={'serviceKey' : 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==', 
                 'QN' : name
                 }
        
        '''
        self.windowBase = Tk()
        self.windowBase.title("BaseData")
        self.windowBase.geometry('1500x600')
        '''
        self.frameBase = Frame(frame)
        self.frameBase.pack()
        

        self.response = requests.get(self.url, params=self.params)
        print(self.response.text)
        self.root = ET.fromstring(self.response.text)
        Header = ["이름","주소","전화번호"]

        # scrollbar=Scrollbar(self.frameBase)
        # scrollbar.pack(side=RIGHT, fill=Y)

        # self.text = Text(self.frameBase, width=150, height=100,wrap=WORD,yscrollcommand=scrollbar.set)
        # self.text.pack()
        # scrollbar.configure(command=self.text.yview)

        for i, col_name in enumerate(Header):
            label = Label(self.frameBase, text=col_name, font=("Helvetica", 20, "bold"))
            label.grid(row=0, column=i)

        row_count = 1

        for item in self.root.iter("item"):
            dutyName = item.findtext("dutyName")        # 이름

            for i, value in enumerate(dutyName):
                label = Label(self.frameBase, text=value, font=("Helvetica", 9))
                label.grid(row=row_count, column=i)   
            row_count += 1                 

    def subDef(self):
        pass

    def Bookmark(self):
        pass
    
    def mapEnergency(self):
        mapUrl = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire'
        self.sumList = []
        mapParams = {'serviceKey' : 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==',
             'Q0' : '서울특별시',
             'pageNo' : '1', 
             'numOfRows' : '100'
             }
        mapResponse = requests.get(mapUrl, params=mapParams)
        mapRoot = ET.fromstring(mapResponse.text)

        for item in mapRoot.iter("item"):
            dataList = []
            dataList.append(item.findtext("dutyName"))    # 이름
            dataList.append(item.findtext("dutyAddr"))    # 주소
            dataList.append(item.findtext("dutyTel1"))    # 번호

            self.sumList.append(dataList) 

    def searchData(self):
        data = self.searchID.get()
        for i in range(len(self.sumList)):
            if data == self.sumList[i][0]:
                self.printData(self.sumList[i])

    def printData(self,data):
        Header = ['이름','주소','번호']

        for i, value in enumerate(Header):
            label = Label(self.frame2, text=value, font=self.fontStyle2)
            label.place(x=50, y=50 + 200*i)   
            

        size = [data[0],data[1],data[2]]
        for i, value in enumerate(size):
            label = Label(self.frame2, text=value, font=self.fontStyle3)
            label.place(x=150, y=50 +200*i) 

    def __init__(self):
        self.window = Tk()
        self.window.title("Emergency")
        self.window.geometry('1280x720')
        self.frame = Frame(self.window)
        self.frame.pack()
        self.fontStyle = font.Font(self.window,size=15,weight='bold',family='Consolas')
        self.fontStyle2 = font.Font(self.window,size=20,weight='bold',family='Consolas')
        self.fontStyle3 = font.Font(self.window,size=11,weight='bold',family='Consolas')

        notebook=ttk.Notebook(self.window, width=800, height=600,padding=2)
        notebook.pack(side='left')        

        #notebook으로 목록구분
        #지도
        frame1=Frame(self.window)
        notebook.add(frame1, text="지도")
        Label(frame1, text="지도", fg='black', font=self.fontStyle2).pack()

        #기본정보(기관ID를 출력하게 해서 ID로 검색하게 만들까?)
        self.frame2=Frame(self.window)
        notebook.add(self.frame2, text="기본정보")
        Label(self.frame2, text="기본정보", fg='black', font=self.fontStyle2).pack()
        self.searchID = Entry(self.frame2, width = 20)
        self.search = Button(self.frame2, text="검색", width=8,command=self.searchData)
        self.search.pack(side = 'bottom')
        self.searchID.pack(side = 'bottom')

        #병실
        frame3=Frame(self.window)
        notebook.add(frame3, text="병실")
        Label(frame3, text="병실", fg='black', font=self.fontStyle2).pack()

        #목록검색
        frame4=Frame(self.window)
        notebook.add(frame4, text="지역검색")
        Label(frame4, text="지역검색", fg='black', font=self.fontStyle2).pack()
        num = 1
        self.base = Button(frame4, text="정보출력", command= lambda : self.baseData(frame4,num), width=8)
        self.prev = Button(frame4, text='이전 페이지',width = 8)
        self.next = Button(frame4, text='다음 페이지', command= lambda : self.baseData(frame4,num+1), width = 8) # num을 더하고 뺄 방법 알아야함
        
        self.prev.place(x = 300, y = 575)
        self.base.place(x = 365, y = 575)
        self.next.place(x = 430, y = 575)

        

        #즐겨찾기
        frame5=Frame(self.window)
        notebook.add(frame5, text="즐겨찾기")
        Label(frame5, text="즐겨찾기한 목록", fg='black', font=self.fontStyle2).pack()
        self.base = Button(frame5, text="정보출력", command= lambda : self.Bookmark())
        self.base.place(x = 250, y = 570)
        self.base.pack(side = 'bottom')
        
        self.name = Entry(self.window, width = 50)
        self.name.place(x=820,y=100)
        self.button1 = Button(self.window, text="지도검색", padx=149,font=self.fontStyle2)
        self.button1.place(x=820,y=120)

        self.button2 = Button(self.window, text="즐겨찾기등록",font=self.fontStyle2)
        self.button2.place(x=1000,y=300)

        self.button3 = Button(self.window, text="텔레그램",font=self.fontStyle2)
        self.button3.place(x=1000,y=500)
        
        self.loadData = Button(self.window, text='데이터 받아오기',font=self.fontStyle2, command=self.mapEnergency)
        self.loadData.place(x=1000,y=500)

        self.window.mainloop()

Emergency()
