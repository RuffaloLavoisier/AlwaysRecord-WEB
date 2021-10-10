import argparse
import datetime
import json
import os
import sys
import threading
from sys import argv

import flask
import requests
from flask import Flask
from flask.templating import render_template
from flask_basicauth import BasicAuth
from flaskext.markdown import Markdown

from CheckDirectory import createFolder
from DeleteFile import delete_file
from IPalarm import sendEmail

app = Flask(__name__)
Markdown(app, extensions=["nl2br", "fenced_code"])

api = "http://ip-api.com/json/"

data = ''  # read ( .md ) init
LogPath = '/home/pi/alwaysSERVER/Test_Server/log/'  # 로그 파일 경로
TargetPath = '/home/pi/alwaysSERVER/AlwaysRecord/'
TargetKeyword = 'days'  # 찾으려는 타켓 키워드
UpdateTime = '2358'  # 업데이트 시간
count_img=""
number_img=0

#now_ip=0
#prev_ip=0
# App Globals (do not edit)
#app = Flask(__name__)
#app.config['BASIC_AUTH_USERNAME'] = 'diaryPI'
#app.config['BASIC_AUTH_PASSWORD'] = 'raspberrypi'
#app.config['BASIC_AUTH_FORCE'] = True

#basic_auth = BasicAuth(app)


#@basic_auth.required
@app.route('/')
def index():
    global data, LogPath,count_img,prev_ip,now_ip
    ip_address = flask.request.remote_addr  # ip 읽어오기
    #now_ip=ip_address
    api_info = requests.get(api+str(ip_address)).json()
    All_param = str("[Victim]:")+str(api_info['query']) \
        +"\n"+str("[ISP]:")+str(api_info['isp']) \
        +"\n"+str("[Organisation]:")+str(api_info['org']) \
        +"\n"+str("[City]:")+str(api_info['city']) \
        +"\n"+str("[Region]:")+str(api_info['region']) \
        +"\n"+str("[Longitude]:")+str(api_info['lon']) \
        +"\n"+str("[Latitude]:")+str(api_info['lat']) \
        +"\n"+str("[Time-zone]:")+str(api_info['timezone']) \
        +"\n"+str("[Zip-code]:")+str(api_info['zip'])+"\n"
    DateNow = datetime.datetime.now()
    LogIpAddress = str(DateNow.strftime("%Y/%m/%d-%H:%M:%S")) + \
        str(" - ")+str(ip_address)+"\n"+str(All_param)  # log ip address with date time
    DateToFileName = DateNow.strftime("%Y-%m-%d-%a")  # 현재 시간을 로그 파일 이름으로

    createFolder(LogPath)  # 해당 경로가 있는지 확인

    FileName = LogPath+DateToFileName  # 현재 시간과 경로를 결합하여 로그 파일 경로 이름 생성

    LogFile = open(FileName, 'a')  # 파일 열기
    LogFile.write(str(LogIpAddress)+str('\n'))  # 파일 쓰기
    LogFile.close()  # 파일 닫기

    delete_file(LogPath, deadline=120)  # 로그가 많으면 삭제하기
    #if now_ip != prev_ip:
    sendEmail() # just tab !
    #    prev_ip=now_ip
    
    return render_template('index.html', data=data,image_file="image/"+count_img)


def dataUpdater():
    global data, TargetKeyword, UpdateTime,count_img,number_img
    #시간이 맞으면 읽어오기
    Start = True  # 처음은 초기화
    while True:
        #읽으려는 파일 알아오기
        DateNow = datetime.datetime.now()

        DateDir = DateNow.strftime("%Y-%m")  # 접근하려는 폴더 날짜
        FineFileName = os.popen('ls -b '+str(TargetPath)+str(
            DateDir)+' | tail -1').read()  # 찾으려는 파일 (이름순 정렬 후 제일 마지막 (최신))
        FineFileName = FineFileName.replace("\n", "")  # 줄바꿈 지우기

        if str(DateNow.strftime("%H%M")) == str(UpdateTime) or Start == True:  # 하루에 마지막에 업데이트 !
            number_img=number_img+1 # sort file counter
            if number_img > int(os.popen("ls -l | grep ^- | wc -l").read()[:-1]):
                number_img=1 # max
            count_img=str(os.popen("ls -b static/image | head -"+str(number_img)+" | tail -1").read()[:-1])
            data = os.popen('sed -n "/'+str(TargetKeyword)+'/,\$p" '+str(TargetPath) +
                            str(DateDir)+str('/')+FineFileName).read()  # 해당하는 행 부터 끝까지 저장하기

        Start = False

if __name__ == "__main__":

    Updater = threading.Thread(target=dataUpdater, args=())  # 로그 그리기

    Updater.daemon = True
    Updater.start()

    app.run(host='0.0.0.0',port=8080, debug=False)


