import datetime
import os
import threading

import flask
from flask import Flask
from flask.templating import render_template
from flaskext.markdown import Markdown

from CheckDirectory import createFolder
from DeleteFile import delete_file

app = Flask(__name__)
Markdown(app, extensions=["nl2br", "fenced_code"])

data = ''  # read ( .md ) init
LogPath = '/home/pi/my_github_project/Test_Server/log/'  # 로그 파일 경로
TargetPath = '/home/pi/my_github_project/AlwaysRecord/'
TargetKeyword='네끼' # 찾으려는 타켓 키워드
UpdateTime='2358' # 업데이트 시간

@app.route('/')
def index():
    global data,LogPath
    ip_address = flask.request.remote_addr  # ip 읽어오기
    DateNow = datetime.datetime.now()
    LogIpAddress = str(DateNow.strftime("%Y/%m/%d-%H:%M:%S"))+str(" - ")+str(ip_address)  # log ip address with date time
    DateToFileName = DateNow.strftime("%Y-%m-%d-%a")  # 현재 시간을 로그 파일 이름으로
    
    createFolder(LogPath)  # 해당 경로가 있는지 확인
    
    FileName = LogPath+DateToFileName  # 현재 시간과 경로를 결합하여 로그 파일 경로 이름 생성

    LogFile = open(FileName, 'a')  # 파일 열기
    LogFile.write(str(LogIpAddress)+str('\n'))  # 파일 쓰기
    LogFile.close()  # 파일 닫기

    delete_file(LogPath, deadline=7)  # 로그가 많으면 삭제하기

    return render_template('index.html', data=data)


def dataUpdater():
    global data,TargetKeyword,UpdateTime
    #시간이 맞으면 읽어오기
    Start = True #처음은 초기화
    while True:
        #읽으려는 파일 알아오기
        DateNow = datetime.datetime.now()

        DateDir = DateNow.strftime("%Y-%m")  # 접근하려는 폴더 날짜
        FineFileName = os.popen('ls -b '+str(TargetPath)+str(
            DateDir)+' | tail -1').read()  # 찾으려는 파일 (이름순 정렬 후 제일 마지막 (최신))
        FineFileName = FineFileName.replace("\n", "")  # 줄바꿈 지우기

        if str(DateNow.strftime("%H%M")) == str(UpdateTime) or Start == True:  # 하루에 마지막에 업데이트 !
            data = os.popen('sed -n "/'+str(TargetKeyword)+'/,\$p" '+str(TargetPath) +
                            str(DateDir)+str('/')+FineFileName).read()  # 해당하는 행 부터 끝까지 저장하기
        
        Start=False


if __name__ == "__main__":

    Updater = threading.Thread(target=dataUpdater, args=())  # 로그 그리기

    Updater.daemon = True
    Updater.start()

    app.run(host='0.0.0.0', port=8080, debug=False)
