# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:34:20 2021

@author: fuwen

"""
import re,requests,time
import sys
reload (sys)
sys.setdefaultencoding('utf-8')

username = "fuwenyue"
password = "123abc123456"

url = "https://www.93hsy.com/member.php"
kgurl = 'https://www.93hsy.com/plugin.php?id=miner:miner'
headers = {"Accept": "","Referer": "https://www.93hsy.com/plugin.php?id=k_misign:sign","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko","Content-Type": "application/x-www-form-urlencoded","Host": "www.93hsy.com","DNT": "1"}
session = requests.session()
post_data = { "fastloginfield": 'username',"username": username,"password": password,"quickforward": 'yes',"handlekey": 'ls'}
a = session.post(url, params={'mod': 'logging','action': 'login','loginsubmit': 'yes','infloat': 'yes','lssubmit': 'yes','inajax': 1}, data=post_data, headers=headers)

def checkin():#签到
    r = session.get(url='https://www.93hsy.com/plugin.php?id=k_misign:sign').text
    formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', r).group(1).encode('ascii')
    url = "https://www.93hsy.com/plugin.php"
    params = {'id': "k_misign:sign",'operation': 'qiandao','formhash': formhash,'format': 'empty','inajax': 1,'ajaxtarget': 'JD_sign'}
    checkin = session.get(url=url, params=params, headers=headers)
    if checkin.status_code == 200:    
        print('已签到')
       
while True:
    rep = session.get(kgurl)
    html = rep.text
    systime = re.findall('GMT\+8, (.*)\r', html)[0]
    print('当前时间',systime)
    shouyi = re.findall('领取收益</a></span>可领收益：(.*?) ', html)[0]
    print('可领取收益%s银币'%shouyi)
    SysSecond = re.findall(r'SysSecond = (.*?);', html)[0]
    SysMin = int(SysSecond)/60
    print('矿工收益剩余时间%s分'%SysMin)
    if len(re.findall('点击签到', html)) >0:
        checkin()  
    if float(shouyi) > 99:#可领取收益大于99时，领取银币。
        rep = session.get('https://www.93hsy.com/plugin.php?id=miner:misc&action=getoutput&infloat=yes&handlekey=miner&inajax=1&ajaxtarget=fwin_content_miner')
        formhash = re.findall('name="formhash" value="(.*?)"', rep.text)[0]
        PostUrl = 'https://www.93hsy.com/plugin.php?id=miner:misc&action=getoutput'
        Data = {'formhash': formhash,'getoutputsubmit': 'true'}
        L = session.post(PostUrl,Data)
        J = re.findall("showmsg\('(.*?)'\);", L.text)[0]
        print('收益领取完成！')
    # 时长奖励
    formhash = re.findall("index&action=award&formhash=(.*?)'", html)[0]
    Long = re.findall('var condition = (.*?);', html)[0]
    Now =  re.findall('var current = (.*?);', html)[0]
    RemainMin = (int(Long) - int(Now))/60
    print('时长剩余时间%s分'%RemainMin)
    if RemainMin==0:
        c = session.get('https://www.93hsy.com/plugin.php?id=gonline:index&action=award&formhash=%s'%formhash)
        print('时长已领取')
    print('----------')
    time.sleep(600)
