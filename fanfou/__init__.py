#coding: utf8

from urlfetch import fetch, setcookielist2cookiestring
import re

class Fanfou(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "http://m.fanfou.com/"
        )
        token = re.search('''name="token".*?value="(.*?)"''', response.body).group(1)
        
        response = fetch(
            "http://m.fanfou.com/",
            data = {
                'loginname': self.username,
                'loginpass': self.password,
                'action': 'login',
                'token': token,
                'auto_login': 'on',
            },
            headers = {
                "Referer": "http://m.fanfou.com/",
            }
        )
        set_cookie = response.msg.getheaders('Set-Cookie')
        self.cookies = setcookielist2cookiestring(set_cookie)
        return response.body

    def update(self, status):
        response = fetch(
            "http://m.fanfou.com/home",
            headers = {
                'Cookie': self.cookies,
                'Referer': "http://m.fanfou.com/home",
            }
        )
        token = re.search('''name="token".*?value="(.*?)"''', response.body).group(1)
        response = fetch(
            "http://m.fanfou.com/",
            data = {
                'content': status,
                'token': token,
                'action': 'msg.post',
            },
            headers = {
                'Cookie': self.cookies,
                'Referer': "http://m.fanfou.com/home",
            }
        )
        return response.body


def pub2fanfou(username, password, status):
    fanfou = Fanfou(username, password)
    fanfou.login()
    fanfou.update(status)

