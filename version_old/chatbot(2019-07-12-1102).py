# -*- coding: utf-8 -*-
import os
import sys
import re
import urllib.request

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from threading import Thread

# 블록 클래스를 사용하는 데 필요한 import 문입니다.
from slack.web.classes import extract_json
from slack.web.classes.blocks import *

# auth_info
SLACK_TOKEN = 'xoxb-692051205782-679678676978-aC2L0D3OrEZ3Y8lpeOrfj4F6'
SLACK_SIGNING_SECRET = 'b747b8aef774792d266ee9adaccaf30f'
client_id = "O1F4aJTMecfTU8KrqzNS"
client_secret = "uzWJPp6XgS"

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# (이하 2019-07-12 수정) 코드 최적화
trans = ['ko_to_en','en_to_ko','ko_to_ja','ko_to_vi','ko_to_fr','ko_to_es','ko_to_id','ko_to_th','ko_to_ru','en_to_ja']
def _papago(text):
    new_text=text.split(",")
    idx = 0
    try:
        #idx = trans.index(new_text[0].replace("<@UKZKYKWUS> ",""))
        idx = trans.index(new_text[0][13:])
    except:
        pass

    if trans[idx] in text:
        new_new_text = ",".join(new_text[1:])

        encount = 0
        kocount = 0

        if trans[idx][:2]  == 'ko':
            for i in new_new_text:
                if ord('a') <= ord(i) <= ord('z'):
                    encount = encount + 1
        # elif trans[idx][:2]  == 'en':
        #     for i in new_new_text:
        #         if ord('가') <= ord(i) <= ord('z'):
        #             encount = encount + 1


        if encount != 0:
            return "한글 입력하세요."
        else:
            
            encText = urllib.parse.quote(new_new_text)
            data = "source=" +trans[idx][:2] + "&target="+trans[idx][-2:] + "&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
            else:
                return ("Error Code:" + rescode)
    
    elif 'help' in text:
        block1 = SectionBlock(
        text="`@ko_to_en` : 한국어->영어"+"\n"+"`@en_to_ko` : 영어->한국어"+"\n"+
        "`@ko_to_ja` : 한국어->일어"+"\n"+
        "`@ko_to_ja` : 한국어->일어"+"\n"+"`@ko_to_vi` : 한국어->베트남어"+"\n"+
        "`@ko_to_fr` : 한국어->프랑스어"+"\n"+
        "`@ko_to_es` : 한국어->스페인어"+"\n"+
        "`@ko_to_id` : 한국어->인도네시아어"+"\n"+
        "`@ko_to_th` : 한국어->태국어"+"\n"+
        "`@ko_to_ru` : 한국어->러시아어"+"\n"+
        "`@en_to_ja` : 영어->일본어"
        )
        block2 = SectionBlock(
        text="`@<명령어>, <문장>` 의 형태로 멘션해주세요."
        )
        my_blocks = [block1,block2]
        slack_web_client.chat_postMessage(
        channel="#ssafy",
        blocks=extract_json(my_blocks)
)
    else:
        return "`@<봇이름> help` 와 같이 멘션해주세요."

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    message = _papago(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        text=message
    )

# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)