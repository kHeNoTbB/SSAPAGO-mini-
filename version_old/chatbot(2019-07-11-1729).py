# -*- coding: utf-8 -*-
import os
import sys
import re
import urllib.request

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# 블록 클래스를 사용하는 데 필요한 import 문입니다.
from slack.web.classes import extract_json
from slack.web.classes.blocks import *

# auth_info
SLACK_TOKEN = 'xoxb-692051205782-679678676978-aC2L0D3OrEZ3Y8lpeOrfj4F6'
SLACK_SIGNING_SECRET = 'b747b8aef774792d266ee9adaccaf30f'
client_id = "O1F4aJTMecfTU8KrqzNS" # 개발자센터에서 발급받은 Client ID 값
client_secret = "uzWJPp6XgS" # 개발자센터에서 발급받은 Client Secret 값

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# (이하 2019-07-12 수정) 코드 최적화

trans = ['ko_to_en','en_to_ko','ko_to_ja','ko_to_vi','ko_to_fr','ko_to_es','ko_to_id','ko_to_th','ko_to_ru','en_to_ja']

# ko to eng
def _papago(text):
    #new_text=text.split(",")
    #new_text = ['trans', '안녕']

    idx = trans.index[text]

    # 1. 한국어->영어
    if trans[idx] in text:
        new_text=text.split(",")
        new_new_text= ",".join(new_text[1:])

        encText = urllib.parse.quote(new_new_text)
        data = "source="+trans[:2] + "&target="+trans[-2:] + "&text=" + encText
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
    
    # # 2. 영어->한국어
    # elif 'en_to_ko' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=en&target=ko&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode)

    # # 3. 한글->일어
    # elif 'ko_to_ja' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=ja&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode)
    
    # # 3. 한글->베트남
    # elif 'ko_to_vi' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=vi&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode)



    # # 4. 한글->프랑스
    # elif 'ko_to_fr' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=fr&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode)   


    # # 5. 한글->스페인
    # elif 'ko_to_es' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=es&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode) 



    # # 6. 한글->인도네시아어
    # elif 'ko_to_id' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=id&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode) 

    # # 7. 한글->태국
    # elif 'ko_to_th' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=th&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode) 

    # # 8. 한글-> 러시아
    # elif 'ko_to_ru' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=ko&target=ru&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode) 

    # # 9. 영어->일본어
    # elif 'en_to_ja' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     data = "source=en&target=ja&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode)

    # #10. 한글->중어
    # elif 'ko_to_ch' in text:
    #     new_text=text.split(",")
    #     new_new_text= ",".join(new_text[1:])

    #     encText = urllib.parse.quote(new_new_text)
    #     var="zh-TW"
    #     data = "source=ko&target=%s&text=" %var + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id",client_id)
    #     request.add_header("X-Naver-Client-Secret",client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #     if(rescode==200):
    #         response_body = response.read()
    #         return (response_body.decode('utf-8')[152:].split("\"")[0].replace(", @UKZKYKWUS.", ""))
    #     else:
    #         return ("Error Code:" + rescode)

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
        text="`@명령어, 문자열`위와 같이 멘션해주세요."
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
