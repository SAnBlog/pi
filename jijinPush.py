import requests
import json
import re

def getInfo(code):
    
    #code = "161726"  # 基金代码
    url = "http://fundgz.1234567.com.cn/js/%s.js"%code
    # 浏览器头
    headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text

    # 正则表达式
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, content)
    # 遍历结果
    for i in search:
         data = json.loads(i)
         print("{} 涨幅: {}".format(data['name'],data['gszzl']))
         return "{} 涨幅: {}".format(data['name'],data['gszzl'])

codes = ['161726','003096','001594','110022','320007','161725']
desp = ''
for code in codes:
    desp+=getInfo(code)+" \n-------------------------------\n"
#以下两个微信推送api,自行申请密钥
requests.get("https://sc.ftqq.com/.send?text=基金每日涨幅&desp="+desp)
requests.get("https://xizhi.qqoq.net/.send?title=基金每日涨幅&content="+desp)
