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
from flask.templating import render_template, render_template_string
from flask_basicauth import BasicAuth
from flaskext.markdown import Markdown
import time
from CheckDirectory import createFolder
from DeleteFile import delete_file
from IPalarm import sendEmail

app = Flask(__name__)
Markdown(app, extensions=["nl2br", "fenced_code"])

api = "http://ip-api.com/json/"
timer_study = ""
data = ''  # read ( .md ) init
LogPath = '/home/pi/alwaysSERVER/Test_Server-link/log'  # 로그 파일 경로
TargetPath = '/home/pi/alwaysSERVER/AlwaysRecord/'
TargetKeyword = 'days'  # 찾으려는 타켓 키워드
UpdateTime = '2358'  # 업데이트 시간
count_img = ""
number_img = 0

# now_ip=0
# prev_ip=0
# App Globals (do not edit)
#app = Flask(__name__)
#app.config['BASIC_AUTH_USERNAME'] = 'diaryPI'
#app.config['BASIC_AUTH_PASSWORD'] = 'raspberrypi'
#app.config['BASIC_AUTH_FORCE'] = True

#basic_auth = BasicAuth(app)


# @basic_auth.required
@app.route('/media_part')
def index():
    global data, LogPath, count_img, prev_ip, now_ip, timer_study
    ip_address = flask.request.remote_addr  # ip 읽어오기
    # now_ip=ip_address
    api_info = requests.get(api+str(ip_address)).json()
    DateNow = datetime.datetime.now()
    LogIpAddress = str(DateNow.strftime("%Y/%m/%d-%H:%M:%S")) + \
        str(" - ")+str(ip_address)+"\n"  # log ip address with date time
    DateToFileName = DateNow.strftime("%Y-%m-%d-%a")  # 현재 시간을 로그 파일 이름으로
    data = "# "+DateToFileName+"\n" + \
        "### Graduation project [Origin Full](https://platform.hoseo.ac.kr/contest/view?idx=248)" + \
        "\n" + \
        "### Graduation project [ENG sub Full](https://youtu.be/pA53EucmKng)" + \
        "\n" + \
        "### Don't click! [website](http://39.124.30.130/)"

    createFolder(LogPath)  # 해당 경로가 있는지 확인

    FileName = LogPath+DateToFileName  # 현재 시간과 경로를 결합하여 로그 파일 경로 이름 생성

    LogFile = open(FileName, 'a')  # 파일 열기
    LogFile.write(str(LogIpAddress)+str('\n'))  # 파일 쓰기
    LogFile.close()  # 파일 닫기

    delete_file(LogPath, deadline=120)  # 로그가 많으면 삭제하기
    # if now_ip != prev_ip:
    sendEmail(ip_address, "profile")  # just tab !
    #    prev_ip=now_ip

    return render_template('index.html', data=data, image_file="image/"+"reva.png", timer=timer_study)


@app.route('/')
def intro():
    ip_address = flask.request.remote_addr
    sendEmail(ip_address, "main")
    print(flask.request.remote_user)
    return render_template('intro.html')


def dataUpdater():
    global data, TargetKeyword, UpdateTime, count_img, number_img, timer_study
    # 시간이 맞으면 읽어오기
    Start = True  # 처음은 초기화
    while True:
        # 읽으려는 파일 알아오기
        DateNow = datetime.datetime.now()

        DateDir = DateNow.strftime("%Y-%m")  # 접근하려는 폴더 날짜
        tomorrow_end = os.popen("date +%F -d tomorrow").read()
        tomorrow_end = tomorrow_end[:-1]
        tomorrow_end_array = tomorrow_end.split("-")
        tomorrow_soon = datetime.datetime(int(tomorrow_end_array[0]), int(
            tomorrow_end_array[1]), int(tomorrow_end_array[2]))
        how_long = tomorrow_soon-DateNow
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        seconds = how_long.seconds - hours * 3600 - minutes * 60
        timer_study = '*Remaining time* => {}days **{}:{}:{}**'.format(
            days, hours, minutes, seconds)


if __name__ == "__main__":

    Updater = threading.Thread(target=dataUpdater, args=())  # 로그 그리기

    Updater.daemon = True
    Updater.start()

    app.run(host='0.0.0.0', port=80, debug=False)
