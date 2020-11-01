import requests
import json


def send_dingtalk_message(msg, dingtalk_token):
    if not dingtalk_token:
        return False

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
    if not pushplus_token:
        return False

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
    if not serverChan_key:
        return False

    r = requests.get("https://sc.ftqq.com/" + serverChan_key
                     + ".send?text=" + text + "&desp=" + desp).json()
    return r["errno"] == 0
