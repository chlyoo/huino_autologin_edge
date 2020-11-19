from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Chrome, Edge
import schedule
import re
import sys
import time
import random
import webbrowser
from config import *
from datetime import datetime


def login(wd):
    #login_page
    wd.get('http://lms.aiha.kr/')
    wd.find_element_by_name('email').send_keys(user_id)
    wd.find_element_by_name('password').send_keys(user_pw)
    wd.find_element_by_class_name('disbtn').submit()
    wd.implicitly_wait(3)


def attend_class(wd,test=False):#출석체크
    wd.get('http://lms.aiha.kr/dashboard/attendance/{}/{}'.format(course_number,user_number))
    att_txt=wd.find_element_by_class_name('content').text#출석 인정 시간이 아닙니다.
    if "출석 인정 시간이 아닙니다." == att_txt:
        print('attendance failed')
        a=random.random()
        if a>=0.5:
            a=random.random()
            print('pass to find zoom url')
            wd.implicitly_wait(3)
            zoom_link_connect(wd,test)
        else:
            a=random.random()
            time.sleep(0.5)    
            attend_class(wd)
    else:
        print('attendance success')
        wd.implicitly_wait(3)
        zoom_link_connect(wd,test)
#zoom 연결
#수업게시판
def zoom_link_connect(wd,test):
    wd.get('http://lms.aiha.kr/course/{}'.format(course_number))
    if test:
        testdate= '2020-11-19'
        a= wd.find_element_by_id(testdate).text
    else:
        a=wd.find_element_by_id(str(datetime.now().date())).text
    try:
        print(a)
        if a != None:
            zoomurl=re.search("(?P<url>https?://zoom[^\s]+)", a).group("url")
            print(zoomurl)
            print('zoom success')
            webbrowser.open(zoomurl)
    except:
        zoom_link_connect(wd,test)
        return 0
    return 0


def automa(test=False):
    wd=Chrome()
    login(wd)
    attend_class(wd,test)


def schedulerrr():
    schedule.every().monday.at(start_time).do(automa)
    schedule.every().tuesday.at(start_time).do(automa)
    schedule.every().wednesday.at(start_time).do(automa)
    schedule.every().thursday.at(start_time).do(automa)
    schedule.every().friday.at(start_time).do(automa)
    while True:
        schedule.run_pending()
        time.sleep(60)
# automa(True)

if datetime.today().weekday()<=4:
    if str(datetime.now().time())>=end_time:
        sys.exit()
    elif str(datetime.now().time())<=init_time:
        schedulerrr()
    else:
        automa()
else:
    sys.exit()
