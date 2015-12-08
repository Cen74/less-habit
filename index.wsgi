# -*- coding: UTF-8 -*- 
import sys
#import os
# sys.setdefaultencoding() does not exist, here!import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from bottle import Bottle, route, run, template, request, get, post, view, debug
import xml.etree.ElementTree as ET

import sae
import hashlib
#import sae.kvdb

#kv = sae.kvdb.Client()

app = Bottle()
debug(True)

application = sae.create_wsgi_app(app)


def check_signature():
    token = 'janet2mm'

    timestamp = request.query.timestamp
    nonce = request.query.nonce
    signature = request.query.signature
    echostr = request.query.echostr

    login_str = ''.join(sorted([token, timestamp, nonce]))
    check_login = hashlib.sha1(login_str).hexdigest()

    if check_login == signature: 
        return echostr
    else: 
        return None


@app.get('/weixin')
def login():
    return check_signature()
   

@app.post('/weixin')
def echo_weixin():
    print request.body.read()
    weixin_msg = ET.fromstring(request.body.read())
    mydict = {child.tag:child.text for child in weixin_msg}
    print mydict

    import time
    mydict['CreateTime'] = int(time.time())

    xml_return = '''
    <xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>{}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{}]]></Content>
    </xml> '''.format(mydict['FromUserName'], mydict['ToUserName'], mydict['CreateTime'], mydict['Content'])

    return xml_return

