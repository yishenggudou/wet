#coding: utf8

from lib import *
from urlfetch import fetch, setcookielist2cookiestring
import re
shorten_re = re.compile(r'''(http://t\.co/\w+)''')

class Twitter(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookies = ''
        
    def login(self):
        response = fetch(
            "https://mobile.twitter.com/session/new",
            headers = {
                'Referer': 'http://mobile.twitter.com/',
            }
        )
        self.authenticity_token = re.search(
            '''name="authenticity_token" .*?value="([^"]+?)"''',
            response.body
        )
        #print self.authenticity_token
        
        response =fetch(
            "https://mobile.twitter.com/session",
            data = {
                'authenticity_token': self.authenticity_token,
                'username': self.username,
                'password': self.password,
            },
            headers = {
                'Referer': "https://mobile.twitter.com/session/new",
            }
        )
        set_cookie = response.msg.getheaders('Set-Cookie')
        self.cookies = etcookielist2cookiestring(set_cookie)
        return response
        
    def update(self, status):
        response = fetch(
            "http://mobile.twitter.com/",
            data = {
                'authenticity_token': self.authenticity_token,
                'tweet[text]': status,
            },
            headers = {
                'Cookie': self.cookies,
                'Referer': "http://mobile.twitter.com/",
            }
        )
        return response


def pub2twitter(username, password, status):
    t = Twitter(username, password)
    t.login()
    t.update(status)

def get_twitter_status(username, prevtime=None):
    import sys
    sys.path.append('..')
    from lib import mb_code
    from datetime import datetime
    if prevtime is not None:
        ptime = datetime.strptime(prevtime, '%a, %d %b %Y %H:%M:%S +0000')
    else:
        ptime = False
        
    url = 'http://twitter.com/statuses/user_timeline/%s.rss' %  username
    data = fetch(url)
    if not data:
        return []
    from xml.dom import minidom
    try:
        tree = minidom.parseString(data)
    except:
        return []
    desc = tree.getElementsByTagName('description')[1:]
    date = tree.getElementsByTagName('pubDate')
    
    statuses = []
    lst = range(len(desc)-1, -1, -1)
    prefix = '%s: ' % username
    prefix_len = len(prefix)
    for i in lst:
        try:
            status = decodeHtmlentities(mb_code(desc[i].childNodes[0].data))
            if status.startswith(prefix): status = status[prefix_len:]
        except: continue
        pubdate = date[i].childNodes[0].data
        if ptime is False or datetime.strptime(pubdate , '%a, %d %b %Y %H:%M:%S +0000') > ptime:
            shortens = shorten_re.findall(status)
            for s in shortens:
                url = unshortenurl(s)
                if url != s: 
                    status = status.replace(s, url)
            statuses.append((status, pubdate))
    
    return statuses

