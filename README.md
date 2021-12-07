# Diary

It's a personal notebook and a program that records who accessed my notebook.  
개인 수첩인 동시에 누가 내 수첩을 접속했는지 확인하는 프로그램입니다.

웹사이트를 활성화하면 일정한 횟수만큼 알람을 주는 페이지가 추가되었습니다. 

## Usage

```
$ python3 sample_flask.py 
```
### Log File Location

`./log` : ip 접속 로그파일 입니다.

### Image  File Location

`./static/image` : Fake Gallery 입니다.

## Better

1.내 수첩을 누가 보는지 확인할 수 있습니다.  
>단순한 ip 주소를 확인하는 것이지만 타인에 대한 가장 원초적인 흥미를 유발시키기에 충분합니다.  

>IP Address 기반 위치정보를 수집합니다.

2.로그파일이 많아지면 자동으로 오래된 파일을 삭제합니다.

## PS

당신이 직접 매일 글을 쓰면서 당신의 미니 블로그처럼 보여줄 수 있습니다.  
이 프로그램의 장점은 `.md` 파일을 그대로 웹에 보여줄 수 있다는 부분 입니다.   