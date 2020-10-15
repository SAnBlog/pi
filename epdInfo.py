#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket 
import requests

logging.basicConfig(level=logging.DEBUG)


def getIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def getOne():
    try:
        s = requests.session()
        s.keep_alive = False
        return s.get("https://v1.hitokoto.cn?max_length=15").json().get("hitokoto")
    except IOError as e:
        logging.info(e)

def getWeather():
        data = requests.get("http://t.weather.itboy.net/api/weather/city/101310101").json()
        if(200 == data.get("status")):
            wendu = data.get("data").get("wendu")
            shidu = data.get("data").get("shidu")
            forecasts = data.get("data").get("forecast")
            date = time.strftime('%Y-%m-%d')
            for info in forecasts:
                if( info.get("ymd") == date):
                    forecast=info.get("high")+info.get("low")
                    time_draw.text((125,0),forecast,font = font15,fill = 0)
                    time_draw.text((10,105),info.get("type"),font = font15,fill = 0)
                    time_draw.text((10,90),info.get("notice"),font = font11,fill = 0)
                    break
        else:
            time_draw.text((10,50),"未获取到天气",font = font15,fill = 0)

def getNews():
        global newCount,news
        if newCount >= len(news):
            newCount = 0
            s = requests.session()
            s.keep_alive = False
            news = s.get("https://api.xiaohuwei.cn/news.php").json()
            print("refresh news")
        print(len(news[newCount].get("title")))
        if len(news[newCount].get("title")) <=15:
            time_draw.text((20,30),news[newCount].get("title"),font = font15,fill = 0)
        else:
            time_draw.text((20,20),str(news[newCount].get("title"))[0:15],font = font15,fill = 0)
            time_draw.text((20,40),str(news[newCount].get("title"))[15:],font = font15,fill = 0)
        newCount+=1
    
try:
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    # Drawing on the image
    font11 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 11)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    
    logging.info("show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    ip = getIp()
    time_draw.text((10,30),ip,font = font20,fill = 0)
    
    #epd.init(epd.FULL_UPDATE)
    #epd.displayPartBaseImage(epd.getbuffer(time_image))
    epd.display(epd.getbuffer(time_image))
    #epd.init(epd.PART_UPDATE)

    newCount = 0
    news = requests.get("https://api.xiaohuwei.cn/news.php").json()
    while (True):
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)
        #time_draw.rectangle((10, 20, 240, 105), fill = 255)

        time_draw.text((10,0),ip,font = font15,fill = 0)
        time_draw.text((10,70),getOne(),font = font15,fill = 0)
        time_draw.text((110, 105), time.strftime('%Y-%m-%d %H:%M'), font = font15, fill = 0)

       # weather
        getWeather()

       # news
        getNews()

        epd.display(epd.getbuffer(time_image))
        time.sleep(180)
    
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()

