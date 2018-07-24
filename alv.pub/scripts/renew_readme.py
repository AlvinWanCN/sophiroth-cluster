#coding:utf-8
import urllib2,time
from lxml import etree
import re,os,subprocess
import sys
reload(sys)
sys.setdefaultencoding('utf8')
host = 'http://tianqi.2345.com'
path = '/today-58362.htm'
url = host + path
content = urllib2.urlopen(url).read()
html = etree.HTML(content)
#本脚本兼容linux下python2
def get_status():  ##获取天气状况
    try:
        weather_status = html.xpath('//*[@id="wrap"]/div[4]/div[1]/div[3]/dl[1]/dd/ul/li[1]/span[2]')[0].text
        if weather_status:
            return weather_status
    except Exception as e:
        print(e)
        return "unknow"

def get_max_temperature():  # 获取最高气温
    # weather_max_temperature=re.findall(r'</b>(-?\d)<i>',str(content))[0]
    try:
        weather_max_temperature = html.xpath('//*[@id="wrap"]/div[4]/div[1]/div[3]/dl[1]/dd/ul/li[2]/span/text()')[
            0]
        if weather_max_temperature:
            return weather_max_temperature
    except Exception as e:
        print(e)
        return "unknow"

def get_min_temperature():  # 获取最低气温
    try:
        weather_min__temperature = re.findall(r'</b>(-?\d+)<i>', str(content))[-1]
        if weather_min__temperature:
            return weather_min__temperature
    except Exception as e:
        print(e)
        return "unknow"

WORK_DIR='/home/alvin/Travel-Notes/'
os.chdir(WORK_DIR)
YearMonth=time.strftime('%Y/%B')
subprocess.call('git pull',shell=True)
subprocess.call('mkdir -p %s'%WORK_DIR+YearMonth,shell=True)
topic = time.strftime('%d %B %Y Alvin\'s Daily')

template = """
========================================
%s
========================================

 Any suggestion, please email alvin.wan.cn@hotmail.com, thanks for your help. :)

|alvin_logo|

.. |logo| image:: https://help.github.com/assets/images/site/favicon.ico
.. |alvin_logo| image:: https://github.com/AlvinWanCN/life-record/raw/master/images/etlucency.png
 :width: 30px

.. |name| replace:: Alvin
.. |weather| replace:: %s
.. |temperature| replace:: %s°~%s°
.. |city| replace:: Shanghai 
.. |range of activity| replace:: Home

.. |time for get up| replace:: 
.. |Time for reach the company| replace:: 
.. |breakfast| replace:: 
.. |lunch| replace:: 
.. |supper| replace:: 
.. contents:: 

Environment
````````
===================== =========  
**City**              |city| 
**Temperature**       |temperature| 
**Weather**           |weather|   
**Range of activity** |range of activity|
===================== ========= 

Health
````````
============================== =========  
**Time for get up**            |time for get up| 
**Time for reach the company** |time for reach the company| 
**Breakfast**                  |breakfast|   
**Lunch**                      |lunch|
**Supper**                     |supper|
============================== ========= 

Today's plan
`````````````````

English study
-------------------
learn a hundred words in Baicizhan

Technology study
--------------------

Today's Log
````````````````

Tomorrow's plan
````````````````````

""" % (topic, get_status(), get_max_temperature(), get_min_temperature())

readme=open('readme.rst','w')
readme.write(template)
readme.close()

subprocess.call('git commit -m "renew readme.rst" readme.rst',shell=True)
subprocess.call('git push origin master',shell=True)