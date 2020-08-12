import win32gui
from selenium import webdriver
import  schedule
import os, re, sys,  time, random
from config import *
from datetime import datetime

def login(wd):
    #login_page
    wd.get('http://lms.aiha.kr/')
    wd.find_element_by_name('email').send_keys(user_id)
    wd.find_element_by_name('password').send_keys(user_pw)
    wd.find_element_by_class_name('disbtn').submit()
    wd.implicitly_wait(3)
#출석체크
def attend_class(wd,test=False):
    wd.get('http://lms.aiha.kr/dashboard/attendance/{}/{}'.format(course_number,user_number))
    att_txt=wd.find_element_by_class_name('content').text#출석 인정 시간이 아닙니다.
    if "출석 인정 시간이 아닙니다." == att_txt:
        print('attendance failed')
        print('pass to find zoom url')
        if random.random()>=0.5:
            zoom_link_connect(wd,test=test)
        else:
            attend_class(wd)
    else:
        print('attendance success')
        zoom_link_connect(wd,test=test)

#zoom 연결
#수업게시판
def zoom_link_connect(wd,test=True):
    wd.get('http://lms.aiha.kr/course/{}'.format(course_number))
    if test:
        testdate= '2020-07-21'
        a= wd.find_element_by_id(testdate).text
    else:
        a=wd.find_element_by_id(str(datetime.now().date())).text
    try:
        zoomurl=re.search("(?P<url>https?://zoom[^\s]+)", a).group("url")
    except:
        zoom_link_connect(wd,test)
        print('zoom success')
        return 0
    os.system('start {}'.format(zoomurl))
    return 0

def automa(test=False):
    wd = webdriver.Edge("edgedriver/msedgedriver.exe")
    login(wd)
    attend_class(wd,test)

def schedulerrr():
    schedule.every().monday.at("09:56").do(automa)
    schedule.every().tuesday.at("09:56").do(automa)
    schedule.every().wednesday.at("09:56").do(automa)
    schedule.every().thursday.at("09:56").do(automa)
    schedule.every().friday.at("09:56").do(automa)
    window=win32gui.FindWindow('ConsoleWindowClass', None)# int value
    win32gui.ShowWindow(window, 0)
    while True:
        schedule.run_pending()
        time.sleep(3)
#automa(test=False)
if datetime.today().weekday()<=4:
    if str(datetime.now().time())>='17:00':
        sys.exit()
    elif str(datetime.now().time())<='09:55':
        schedulerrr()
    else:
        automa()
else:
    sys.exit()
