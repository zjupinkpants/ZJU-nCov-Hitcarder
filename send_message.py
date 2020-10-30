import requests
import json


def send_dingtalk_message(msg, dingtalk_token):
    dingtalk_url = 'https://oapi.dingtalk.com/robot/send?access_token='+dingtalk_token
    data = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "isAtAll": False
        }
    }
    header = {'Content-Type': 'application/json'}

    r = requests.post(dingtalk_url,
                      data=json.dumps(data), headers=header).json()
    return r["errcode"] == 0


def send_pushplus_message(title, content, pushplus_token):
    pushplus_url = 'http://pushplus.hxtrip.com/customer/push/send'
    data = {
        "token": pushplus_token,
        "title": title,
        "content": content
    }
    headers = {'Content-Type': 'application/json'}

    r = requests.post(pushplus_url, data=json.dumps(data),
                      headers=headers).json()
    return r["code"] == 200


def send_serverChan_message(text, desp, serverChan_key):
    r = requests.get("https://sc.ftqq.com/" + serverChan_key
                     + ".send?text=" + text + "&desp=" + desp).json()
    return r["errno"] == 0

