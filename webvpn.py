import os
from jsbn import RSAKey
import xmltodict
import requests
from fake_useragent import UserAgent


class WebVPN:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sess = requests.Session()

        ua = UserAgent(verify_ssl=False)
        self.sess.headers['User-Agent'] = ua.chrome

    def login(self):
        base_url = 'https://webvpn.zju.edu.cn/'
        login_url = 'https://webvpn.zju.edu.cn/portal/'
        login_auth_url = 'https://webvpn.zju.edu.cn/por/login_auth.csp?apiversion=1'
        login_psw_url = 'https://webvpn.zju.edu.cn/por/login_psw.csp?anti_replay=1&encrypt=1&apiversion=1'

        # Get RSA_ENCRYPT_KEY and CSRF_RAND_CODE
        r = self.sess.get(login_auth_url)

        tree = xmltodict.parse(r.content)
        self.auth = dict(tree['Auth'])
        # print(self.auth["RSA_ENCRYPT_KEY"], self.auth["RSA_ENCRYPT_EXP"],
        #       self.auth["CSRF_RAND_CODE"], self.auth["TwfID"])

        # Encrypt password
        encrypt_data = self.password + '_' + self.auth["CSRF_RAND_CODE"]
        rsa = RSAKey()
        rsa.setPublic(self.auth["RSA_ENCRYPT_KEY"], "10001")
        self.auth["svpn_password"] = rsa.encrypt(encrypt_data)
        # print(self.auth["svpn_password"])

        # Login
        data = {
            "svpn_name": self.username,
            "svpn_req_randcode": self.auth["CSRF_RAND_CODE"],
            "svpn_password": self.auth["svpn_password"]
        }
        cookies = {"TWFID": self.auth["TwfID"]}
        headers = {
            "Origin": base_url,
            "Referer": login_url,
        }
        r = self.sess.post(login_psw_url, data=data,
                           cookies=cookies, headers=headers)

        print(r.status_code)
        print(r.content.decode())
        self.TWFID = self.sess.cookies.get_dict()['TWFID']
        return


if __name__ == "__main__":
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']

    vpn = WebVPN(username, password)
    vpn.login()

    url = 'http://zjuam-zju-edu-cn-s.webvpn.zju.edu.cn:8001/cas/login?service=https%3A%2F%2Fhealthreport.zju.edu.cn%2Fa_zju%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fhealthreport.zju.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex%26from%3Dwap'
    # url = 'http://healthreport-zju-edu-cn-s.webvpn.zju.edu.cn:8001/ncov/wap/default/index'
    r = vpn.sess.get(url)
    print(r.status_code)
    print(r.content.decode())
