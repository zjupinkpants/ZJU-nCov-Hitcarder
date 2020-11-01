import os
import daka
import send_message


if __name__ == "__main__":
    username = os.environ['INPUT_USERNAME']
    password = os.environ['INPUT_PASSWORD']

    if daka.main(username, password):
        msg = '打卡成功'
    else:
        msg = '打卡失败'

    try:
        if send_message.send_dingtalk_message(
                msg, os.environ['INPUT_DINGTALK_TOKEN']):
            print('send_dingtalk_message_success')
        else:
            print('send_dingtalk_message_fail')
    except:
        print('send_dingtalk_message_error')

    try:
        if send_message.send_serverChan_message(
                msg, '', os.environ['INPUT_SERVERCHAN_KEY']):
            print('send_serverChan_message_success')
        else:
            print('send_serverChan_message_fail')
    except:
        print('send_serverChan_message_error')

    try:
        if send_message.send_pushplus_message(
                msg, '', os.environ['INPUT_PUSHPLUS_TOKEN']):
            print('send_pushplus_message_success')
        else:
            print('send_pushplus_message_fail')
    except:
        print('send_pushplus_message_error')
