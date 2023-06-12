# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import requests
import xml.etree.ElementTree as ET
import tkinter.ttk #notebook사용
from PIL import Image, ImageTk
import io
import os
from googlemaps import Client
import matplotlib.pyplot as plt #그래프 그리기
import matplotlib               #그래프 그리기
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #그래프
from matplotlib.figure import Figure                            #그래프
import spam
import numpy as np

class Emergency:
    def PrintList(self,frame,Gu):
        url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire'

        params ={'serviceKey' : 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==', 
                 'Q0' : '서울특별시',
                 'Q1' : Gu ,
                 'PageNo' : '1',
                 'numOfRows' : '100'
                 }
       
        if hasattr(self, 'frameBase'):
            self.frameBase.destroy()
        
        self.frameBase = Frame(frame)
        self.frameBase.pack()

        response = requests.get(url, params=params)
        root = ET.fromstring(response.text)
        Header = ["이름","주소","전화번호"]

        for i, col_name in enumerate(Header):
            label = Label(self.frameBase, text=col_name, font=("Helvetica", 20, "bold"))
            label.grid(row=0, column=i)

        row_count = 1

        for item in root.iter("item"):
            dutyName = item.findtext("dutyName")        # 이름
            dutyAddr = item.findtext("dutyAddr")        # 주소
            dutyTel1 = item.findtext("dutyTel1")        # 전화번호

            sub = dutyAddr.split(' ', 4)
            sub2 = []
            for i in range(4):
                if (i == 3):
                    s = str(sub[i])
                    a = s.replace(',','') 
                    sub2.append(a)
                else:
                    sub2.append(sub[i])
            Address = " ".join(sub2)
            data = [dutyName, Address, dutyTel1]
            for i, value in enumerate(data):
                label = Label(self.frameBase, text=value, font=self.fontStyle3)
                label.grid(row=row_count, column=i)   
            row_count += 1     
    
    def Listcombobox(self,frame):      # 지역검색에 사용할 콤보박스
        sidoList = ['강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구'
                    ,'노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구','성동구'
                    ,'성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구']
        combobox = ttk.Combobox(frame)
        combobox.config(height=5)           # 높이 설정
        combobox.config(values=sidoList)    # 나타낼 항목 리스트(a) 설정
        combobox.config(state="readonly")   # 콤보 박스에 사용자가 직접 입력 불가
        combobox.bind("<<ComboboxSelected>>", lambda event : self.PrintList(frame,combobox.get()))
        combobox.pack(side = 'bottom')

    def MakeGraph(self):
        #canvas에 값이 있을경우 canvas 지우기
        if hasattr(self,'canvas'):
            self.canvas.get_tk_widget().pack_forget()

        # 한글깨짐현상 해결(그래프)
        matplotlib.rcParams['font.family'] = 'Malgun Gothic'  
        label = ['응급실', '일반중환자실', '신생아중환자실', '수술실']
        x = np.arange(len(label))
        y = []

        # 이름 입력 받기
        name = spam.check(self.Searchname.get())

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
        for element in info_root.findall('.//item'):
            hperyn_element = element.find('hperyn')
            hpicuyn_element = element.find('hpicuyn')
            hpnicuyn_element = element.find('hpnicuyn')
            hpopyn_element = element.find('hpopyn')

            hperyn = int(hperyn_element.text) if hperyn_element is not None else 0
            hpicuyn = int(hpicuyn_element.text) if hpicuyn_element is not None else 0
            hpnicuyn = int(hpnicuyn_element.text) if hpnicuyn_element is not None else 0
            hpopyn = int(hpopyn_element.text) if hpopyn_element is not None else 0

            y = [hperyn, hpicuyn, hpnicuyn, hpopyn]

        # Matplotlib Figure 생성
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(x, y)
        ax.set_xticks(x)
        ax.set_xticklabels(label, fontsize='10')

        # Figure를 Tkinter Canvas에 표시
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def mapEnergency(self):
        mapUrl = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire'
        self.sumList = []
        self.hosName = []
        mapParams = {'serviceKey' : 'T6bl9o5oNuqX7IGg2CLG3Ee3pYpw8oX1TR2sngCL9PDloZBAE6rw7drYPb/K2gIzGOyGzOPAxFJiYhMZcRQ+Lg==',
             'Q0' : '서울특별시',
             'pageNo' : '1', 
             'numOfRows' : '100'
             }
        mapResponse = requests.get(mapUrl, params=mapParams)
        mapRoot = ET.fromstring(mapResponse.text)

        for item in mapRoot.iter("item"):
            dataList = {
                "name": item.findtext("dutyName"),  # 병원 이름
                "address": item.findtext("dutyAddr"),  # 병원 주소
                "number": item.findtext("dutyTel1"),  # 번호
                "lng": item.findtext("wgs84Lon"),  # 경도
                "lat": item.findtext("wgs84Lat"),  # 위도
            }
            self.hosName.append(item.findtext("dutyName"))
            self.sumList.append(dataList)

    def searchName(self):
        self.num = 2
        self.first = False
        newData = spam.check(self.searchID.get())

        if newData not in self.hosName:
            messagebox.showinfo("오류", "없는 기관입니다.")
            return

        for hosData in self.sumList:
            if newData == hosData['name']:
                self.printData(hosData)
                guList = []
                data1 = hosData['address'].split(' ', 4)
                for i in range(4):
                    guList.append(data1[i])
                self.zeroPlace = " ".join(guList)
        self.mapLoad()

    def printData(self,data):
        Header = ['이름','주소','번호']

        for widget in self.frame2.winfo_children():
            if isinstance(widget, Label):
                widget.destroy()

        for i, value in enumerate(Header):
            label = Label(self.frame2, text=value, font=self.fontStyle2)
            label.place(x=30, y=50+40*i)  

        size = [data['name'],data['address'],data['number']]
        for i, value in enumerate(size):
            label = Label(self.frame2, text=value, font=self.fontStyle3)
            label.place(x=120, y=50+40*i) 

    def mapLoad(self):
        Google_API_Key = ''
        gmaps = Client(key=Google_API_Key)
        if (self.first == True):
            self.zeroPlace = "경기 시흥시 산기대학로 237 한국공학대학교"

        seoul_center = gmaps.geocode(self.zeroPlace)[0]['geometry']['location']
        seoul_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={seoul_center['lat']},{seoul_center['lng']}&zoom={self.zoom}&size={self.xSize}x{self.ySize}&maptype=roadmap" 
        
        for hos in self.sumList:
            if hos['lat'] and hos['lng']:
                lat, lng = float(hos['lat']), float(hos['lng'])
                marker_url = f"&markers=color:red%7C{lat},{lng}"
                seoul_map_url += marker_url

        if (self.num == 2):
            self.zoom = 18
            response = requests.get(seoul_map_url+'&key='+Google_API_Key)
            image = Image.open(io.BytesIO(response.content))
            photo = ImageTk.PhotoImage(image)
            map_label = Label(self.frame2, image=photo)
            map_label.pack()
            map_label.configure(image=photo)
            map_label.image = photo
            map_label.place(x=400,y=125)

        elif (self.num == 3):
            self.zoom = 18
            response = requests.get(seoul_map_url+'&key='+Google_API_Key)
            image = Image.open(io.BytesIO(response.content))
            photo = ImageTk.PhotoImage(image)
            map_label = Label(self.frame2, image=photo)
            map_label.pack()
            map_label.configure(image=photo)
            map_label.image = photo
            map_label.place(x=400,y=125)

    def teleOn(self):
        import noti
        import teller

    def zoom_in(self):
        self.zoom += 1
        self.mapLoad()

    def zoom_out(self):
        self.zoom -= 1
        self.mapLoad()
    
    def BookMark(self):
        check = False
        newData = spam.check(self.baseName.get())
        if newData == '':
            messagebox.showinfo("오류", "내용을 입력해 주세요")
            return
        for hosData in self.sumList:
            if newData not in self.saveList:
                if newData == hosData['name']:
                    self.saveList.append(newData)
                    data = str(hosData['name']+' / '+hosData['address']+' / '+hosData['number']+'\n')
                    file_path = os.path.join(os.getcwd(), "즐겨찾기.txt")
                    file = open(file_path, "a")
                    file.write(data)
                    file.close()
                    messagebox.showinfo("성공", "저장 성공")
                    return
            else:
                messagebox.showinfo("오류", "이미 즐겨찾기가 되어 있습니다.")
                return
        if (check == False):
            messagebox.showinfo("오류", "올바른 병원 이름을 입력해 주세요")
            return
        name = spam.check(self.Searchname.get())

    def loadFile(self):
        # 파일을 읽기 모드로 엽니다
        with open("즐겨찾기.txt", "r") as file:
            # 파일로부터 데이터를 읽습니다
            data = file.read()
        
        a = data.split('\n')

        # 기존의 리스트 박스와 스크롤바 삭제
        if hasattr(self, 'dataList'):
            self.dataList.pack_forget()
            self.dataList.destroy()
        if hasattr(self, 'scrollbar'):
            self.scrollbar.destroy()

        self.dataList = Listbox(self.frame5, width=90,font=self.fontStyle4)
        self.dataList.delete(0, END)
        
        for item in a:
            self.dataList.insert(END, item)  # 끝에 아이템 추가

        self.scrollbar = Scrollbar(self.frame5)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # 스크롤바와 병원 목록 연결
        self.dataList.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.dataList.yview)

        self.dataList.pack()

    def delBookMark(self):
        file_path = os.path.join(os.getcwd(), "즐겨찾기.txt")
        file = open(file_path, "w")
        file.close()
        self.saveList.clear()
        messagebox.showinfo("성공", "삭제 성공")
        return
    
    def MainInfo(self,frame):
        Label(frame, text="1.MAIN", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="메인화면입니다. 상단의 엠뷸런스아이콘을 클릭하여 EMERGENCY프로그램의 설명을 출력할 수 있습니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="2.기본정보", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="응급기관 이름을 입력하여 병원이름,병원주소,전화번호,지도상 위치를 확인할 수 있습니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="우측 하단의 확대,축소 버튼을 이용하여 검색한 응급기관지도를 확대 및 축소할 수 있습니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="3.병실", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="응급기관 이름을 입력하여 응급실, 일반중환자실, 신생아중환자실, 수술실의 갯수여부를 그래프상으로 확인할 수 있습니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="4.목록검색", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="서울특별시의 구를 선택하여 해당 구에 있는 응급기관의 목록을 출력합니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="5.즐겨찾기등록 및 삭제", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="등록 : 즐겨찾기등록 버튼 위의 입력창에 응급기관명을 입력하고 버튼을 누르면 목록에 추가됩니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="삭제 : 즐겨찾기삭제 버튼을 누르면 즐겨찾기목록이 전부 삭제됩니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="출력 : 하단의 정보출력버튼을 누르면 즐겨찾기목록에 저장해둔 응급기관의 정보가 출력됩니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="6.텔레그램", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="텔레그램 버튼을 누르면 Final_Hospital_bot에게 텔레그램메세지로", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="'병원 출력'을 입력하면 서울특별시내의 응급기관목록을 전체출력합니다", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="또 응급기관명을 입력하면 그래프로 나타내었던 병실의 수를 텍스트로 받을 수 있습니다.", fg='black', font=self.fontStyle4).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)
        Label(frame, text="", fg='black', font=self.fontStyle3).pack(side=TOP, anchor=NW)

    def __init__(self):
        self.window = Tk()
        self.window.title("Emergency")
        self.window.geometry('1280x720')
        self.window.configure(bg="white")
        self.frame = Frame(self.window)
        self.frame.configure(bg="white")
        self.frame.pack()
        self.fontStyle = font.Font(self.window,size=15,weight='bold',family='Consolas')
        self.fontStyle2 = font.Font(self.window,size=20,weight='bold',family='Consolas')
        self.fontStyle3 = font.Font(self.window,size=11,weight='bold',family='Consolas')
        self.fontStyle4 = font.Font(self.window,size=9,family='Consolas')

        self.notebook=ttk.Notebook(self.window, width=800, height=550,padding=2)
        self.notebook.pack(side='left')        

        # notebook으로 목록구분
        # Main화면 출력
        self.num = 1
        self.frame1=Frame(self.window)
        self.notebook.add(self.frame1, text="MAIN")
        emimage = PhotoImage(file="엠뷸런스.gif")
        small_image = emimage.subsample(8)
        container = Frame(self.frame1)
        container.pack(side=TOP)
        mainbutton = Button(container, image=small_image, command= lambda : self.MainInfo(self.frame1))
        mainbutton.pack(side=RIGHT)
        Label(container, text="EMERGENCY", fg='black', font=self.fontStyle2).pack()

        # 기본정보(기관ID를 출력하게 해서 ID로 검색하게 만들까?)
        self.frame2=Frame(self.window)
        self.notebook.add(self.frame2, text="기본정보")
        Label(self.frame2, text="기본정보", fg='black', font=self.fontStyle2).pack()
        self.searchID = Entry(self.frame2, width = 20)
        self.search = Button(self.frame2, text="검색", width=8,command=lambda : self.searchName())
        self.search.pack(side = 'bottom')
        self.searchID.pack(side = 'bottom')

        # 병실
        frame3=Frame(self.window)
        self.notebook.add(frame3, text="병실")
        Label(frame3, text="병실", fg='black', font=self.fontStyle2).pack()
        self.frame3 = frame3  # self.frame3에 frame3 저장
        self.Searchname = Entry(frame3, width = 20)
        self.Graph = Button(frame3, text="검색", width=8, command= lambda : self.MakeGraph())
        self.Graph.pack(side = 'bottom')
        self.Searchname.pack(side = 'bottom')

        #목록검색
        frame4=Frame(self.window)
        self.notebook.add(frame4, text="목록검색")
        Label(frame4, text="목록검색", fg='black', font=self.fontStyle2).pack()
        self.Listcombobox(frame4)

        # 즐겨찾기
        self.frame5=Frame(self.window)
        self.notebook.add(self.frame5, text="즐겨찾기")
        Label(self.frame5, text="즐겨찾기한 목록", fg='black', font=self.fontStyle2).pack()
        self.base = Button(self.frame5, text="정보출력", command= lambda : self.loadFile())
        self.base.place(x = 250, y = 770)
        self.base.pack(side = 'bottom')
        
        # 즐겨찾기 등록
        self.baseName = Entry(self.window, width=40)
        self.baseName.place(x=890,y=350)
        self.button2 = Button(self.window, text="즐겨찾기등록", padx=122, font=self.fontStyle2, command= lambda : self.BookMark())
        self.button2.place(x=820,y=370)

    
        self.button3 = Button(self.window, text="즐겨찾기삭제", padx=122, font=self.fontStyle2, command= lambda : self.delBookMark())
        self.button3.place(x=820,y=430)

        self.button4 = Button(self.window, text="텔레그램", padx = 149, font=self.fontStyle2, command= lambda : self.teleOn())
        self.button4.place(x=820,y=490)
        
        zoom_in_button = Button(self.window, text="확대(+)", font=self.fontStyle2, command=self.zoom_in)
        zoom_in_button.place(x=880,y=550)
        zoom_out_button = Button(self.window, text="축소(-)", font=self.fontStyle2, command=self.zoom_out)
        zoom_out_button.place(x=1070,y=550)

        crossimage = PhotoImage(file="십자가.gif")
        #crosssmall_image = crossimage.subsample(4)
        cross = Label(self.window,image=crossimage)
        cross.place(x=925,y=80)

        self.mapEnergency()

        self.saveList = []
        self.zoom = 18
        self.first = True
        self.xSize = 375
        self.ySize = 375
        self.mapLoad()
        
        self.window.mainloop()

Emergency()