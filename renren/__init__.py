#coding: utf8

from urlfetch import fetch, setcookielist2cookiestring
import re

class Renren(object):
    origURL = "http://www.renren.com/SysHome.do"
    domain = "renren.com"
    login_action = "http://www.renren.com/PLogin.do"
    update_action = "http://status.renren.com/doing/updateNew.do"
    comment_action = "http://gossip.renren.com/gossip.do"
    log_comment_action = "http://blog.renren.com/PostComment.do"
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            self.login_action,
            data = {
                'email':self.username,
                'password':self.password,
                'autoLogin':'true',
                'origURL':self.origURL,
                'domain':self.domain,
            }
        )
        self.token = re.search("get_check:'([^']*)'", response.body).group(1)
        self.id = re.search(r'''"id" : (\d+)''', response.body).group(1)
        set_cookie = response.msg.getheaders('Set-Cookie')
        self.cookies = etcookielist2cookiestring(set_cookie)
        return response
        
    def update(self, status):
        response = fetch(
            self.update_action,
            data = {
                'content': status,
                'isAtHome': '1',
                'requestToken': self.token,
            },
            headers = {
                'Referer': 'http://status.renren.com/ajaxproxy.htm',
                'Cookie': self.cookies,
            }
        )
        return response


def pub2renren(username, password, status):
    renren = Renren(username, password)
    renren.login()
    renren.update(status)

