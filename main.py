from selenium import webdriver
import os
import re
from config import *
from datetime import datetime
import schedule
import time
def login(wd):
    #login_page
    wd.get('http://lms.aiha.kr/')
    wd.find_element_by_name('email').send_keys(아이디)
    wd.find_element_by_name('password').send_keys(비밀번호)
    wd.find_element_by_class_name('disbtn').submit()
    wd.implicitly_wait(3)
#출석체크
def attend_class(wd):
    wd.get('http://lms.aiha.kr/dashboard/attendance/77/1804')
    att_txt=wd.find_element_by_class_name('content').text#출석 인정 시간이 아닙니다.
    if "출석 인정 시간이 아닙니다." == att_txt:
        print('attendance failed')
        attend_class()
    else:
        print('attendance success')
        zoom_link_connect(False)

#zoom 연결
#수업게시판
def zoom_link_connect(wd,test=True):
    wd.get('http://lms.aiha.kr/course/77')
    if test:
        testdate= '2020-07-21'
        a= wd.find_element_by_id(testdate).text
    else:
        a=wd.find_element_by_id(str(datetime.now().date())).text
    try:
        zoomurl=re.search("(?P<url>https?://[^\s]+)", a).group("url")
    except:
        zoom_link_connect(wd,test)
    wd.get(zoomurl)
    os.system('start {}'.format(zoomurl))
#    wd.switch_to.alert()

def automa():
    wd = webdriver.Edge("edgedriver/msedgedriver.exe")
    login(wd)
    attend_class(wd)
    zoom_link_connect(wd,test=False)


schedule.every().monday.at("09:50").do(automa)
schedule.every().tuesday.at("09:50").do(automa)
schedule.every().wednesday.at("09:50").do(automa)
schedule.every().thursday.at("09:50").do(automa)
schedule.every().friday.at("09:50").do(automa)

while True:
    schedule.run_pending()
    time.sleep(30)