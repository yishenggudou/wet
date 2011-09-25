#coding: utf8

from urlfetch import fetch, setcookielist2cookiestring
import re

class Douban(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "http://m.douban.com/"
        )
        m = re.search('''href="/\?session=([^'"]+?)"''', response.body)
        self.session = m.group(1)
        #print self.session
        
        response = fetch(
            "http://m.douban.com/",
            data = {
                'form_email': self.username,
                'form_password': self.password,
                'redir': '',
                'user_login': '登录',
                'session': self.session
            },
            headers = {
                'Referer': 'http://m.douban.com/',
            }
        )
        set_cookie = response.msg.getheaders('Set-Cookie')
        self.cookies = setcookielist2cookiestring(set_cookie)
        return response
        
    def update(self, status):
        response = fetch(
            "http://m.douban.com/",
            data = {
                'mb_text': status,
                'session': self.session
            },
            headers = {
                'Referer': 'http://m.douban.com/',
                'Cookie': self.cookies,
            }
        )
        return response
        

def pub2douban(username, password, status):
    douban = Douban(username, password)
    douban.login()
    douban.update(status)
    
