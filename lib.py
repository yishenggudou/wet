def decodeHtmlentities(string):
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]
    
def get_path(filename=None):
    import os.path
    HERE = os.path.dirname(os.path.abspath(__file__))
    if filename is not None:
        HERE = os.path.join(HERE, filename)
    return HERE   

def load_prev_time(id):
    id = get_path(id)
    try:
        return open(id, 'r').read().strip()
    except:
        open(id, 'w').write('Thu, 10 Feb 2011 10:08:49 +0000')
    return 'Thu, 10 Feb 2011 10:08:49 +0000'

def save_prev_time(id, s):
    open(get_path(id), 'w').write(s)

def mb_code(string, coding="utf-8"):
    if isinstance(string, unicode):
        return string.encode(coding)
    for c in ('utf-8', 'gb2312', 'gbk', 'gb18030'):
        try:
            return string.decode(c).encode(coding)
        except:
            pass
    return string
    
def log(string):
    from time import strftime
    timestamp = strftime("%Y-%m-%d %H:%M:%S")
    log_file = get_path('log')
    with open(log_file, 'a+') as f:
        f.write("[%s] %s\n" % (timestamp, string))
        
def str2js_str(str):
    str = mb_code(str)
    str = unicode(str)
    str = repr(str)
    if str:
        str[2:-1]
    return str

def joinpath(d, f):
    from os.path import sep
    return sep.join([d, f])

def writeto(path, data):
    fh = open(path, 'w')
    fh.write(data)
    fh.close()
    
def readfrom(path):
    fh = open(path, 'r')
    data = fh.read()
    fh.close()
    return data
    
def dumpto(path, obj):
    import pickle
    fh = open(path, 'wb')
    pickle.dump(obj, fh)
    fh.close()
    
def loadfrom(path):
    import pickle
    fh = None
    try:
        fh = open(path, 'rb')
        obj = pickle.load(fh)
    except Exception, e:
        obj = None
    finally:
        if fh: fh.close()
    return obj
    
def isreadablefile(path):
    import os
    return os.access(path, os.R_OK)
    
def touch(path):
    import os
    try:
        os.utime(path, None)
    except:
        open(path, 'a').close()
        
def mv(f, t):
    import shutil
    shutil.move(f, t)

def unshortenurl(short):
    from urllib import URLopener
    opener = URLopener()
    try:
        opener.open(short)
    except IOError, e:
        f = e
    try:
        f = e.args[3]
        return f.dict['location']
    except:
        return short
        
