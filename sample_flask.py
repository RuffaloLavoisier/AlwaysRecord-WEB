from flask import Flask
import flask
import datetime
from flask.templating import render_template
from DeleteFile import delete_file
from CheckDirectory import createFolder
from flaskext.markdown import Markdown
import os


app = Flask(__name__)
Markdown(app, extensions=["nl2br", "fenced_code"])

data='' # read .md

# init
Nowdate= datetime.datetime.now().strftime("%Y-%m") # 접근하려는 폴더 날짜 
FineFileName=os.popen('ls -b /home/pi/my_github_project/AlwaysRecord/'+str(Nowdate)+' | tail -1').read() # 찾으려는 파일 (이름순 정렬 후 제일 마지막 (최신))
FineFileName=FineFileName.replace("\n", "") #줄바꿈 지우기
data=os.popen('sed -n "/네끼/,\$p" '+'/home/pi/my_github_project/AlwaysRecord/'+str(Nowdate)+str('/')+FineFileName).read()# 해당하는 행 부터 끝까지 저장하기

@app.route('/')
def index():
    global data
    ip_address = flask.request.remote_addr  # ip 읽어오기
    LogIpAddress = str(datetime.datetime.now().strftime(
        "%Y/%m/%d-%H:%M:%S"))+str(" - ")+str(ip_address)  # log ip address with date time
    DateToFileName = datetime.datetime.now().strftime(
        "%Y-%m-%d-%a")  # 현재 시간을 로그 파일 이름으로
    path = '/home/pi/my_github_project/Test_Server/log/'  # 로그 파일 경로
    createFolder(path)  # 해당 경로가 있는지 확인
    FileName = path+DateToFileName  # 현재 시간과 경로를 결합하여 로그 파일 경로 이름 생성
    
    LogFile = open(FileName, 'a')  # 파일 열기
    LogFile.write(str(LogIpAddress)+str('\n'))  # 파일 쓰기
    LogFile.close()  # 파일 닫기

    delete_file(path, deadline=7)  # 로그가 많으면 삭제하기

    # sed -n "/희망/,\$p" 2021-07-14-수요일.md > test
    # 일기 파일을 읽고서 파이썬 마크다운에 넣는다 쉘 스크립트

    #시간이 맞으면 읽어오기

    #읽으려는 파일 알아오기
    Nowdate= datetime.datetime.now().strftime("%Y-%m") # 접근하려는 폴더 날짜 
    FineFileName=os.popen('ls -b /home/pi/my_github_project/AlwaysRecord/'+str(Nowdate)+' | tail -1').read() # 찾으려는 파일 (이름순 정렬 후 제일 마지막 (최신))
    FineFileName=FineFileName.replace("\n", "") #줄바꿈 지우기
    
    if int(datetime.datetime.now().strftime("%H%M"))==2358:
        data=os.popen('sed -n "/네끼/,\$p" '+'/home/pi/my_github_project/AlwaysRecord/'+str(Nowdate)+str('/')+FineFileName).read()# 해당하는 행 부터 끝까지 저장하기

    #마크다운을 html로 내보내기 위한 방향 
    #MarkDownDiary = open("templates/index.md", 'r')
    #data = MarkDownDiary.read()
    #MarkDownDiary.close()

    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
