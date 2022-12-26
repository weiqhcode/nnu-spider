# -*- coding=UTF-8 -*-
# @Time : 2022/11/20 16:17
# @Author : weiqh
# @File : nnu_spider.py
# @Software : PyCharm
import os
import sys
import time
import uuid
import io
from io import BytesIO
import execjs
import pymongo
import requests
from PIL import Image
import base64
import pandas as pd
import logging
# 获取登录代码 URL
url_code = 'http://jw.nnxy.cn/Logon.do?method=logon&flag=sess'

# 获取验证码 URL
url_get_verification_code = 'http://jw.nnxy.cn/verifycode.servlet'

# 登录 URL
url_login = 'http://jw.nnxy.cn/Logon.do?method=logon'

url_cookie = 'http://jw.nnxy.cn/'
user_name = '学号'
password = '密码'
text = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
# urlBaiDu = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret='
#
SecretKey = '百度AI平台SecretKey'
ApiKey = '百度AI平台ApiKey'

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
}

semester = '2022-2023-1'
week = '14'

Cookie = {}
data = {}

log_file_name = 'MyLogger'

# 创建logger对象
logger = logging.getLogger('log_file_name')
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')
# 创建日志输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建日志输出目标
file_handler = logging.FileHandler('logs.txt')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.info('日志启动成功')



def show_logo():
    print('''

                                                       ,---,     
                                  ,--,  ,----.   ,--.' |     
                 .---.          ,--.'| /   /  \-.|  |  :     
                /. ./|          |  |, |   :    :|:  :  :     
             .-'-. ' |   ,---.  `--'_ |   | .\  .:  |  |,--. 
            /___/ \: |  /     \ ,' ,'|.   ; |:  ||  :  '   | 
         .-'.. '   ' . /    /  |'  | |'   .  \  ||  |   /' : 
        /___/ \:     '.    ' / ||  | : \   `.   |'  :  | | | 
        .   \  ' .\   '   ;   /|'  : |__`--'""| ||  |  ' | : 
         \   \   ' \ |'   |  / ||  | '.'| |   | ||  :  :_:,' 
          \   \  |--" |   :    |;  :    ; |   | :|  | ,'     
           \   \ |     \   \  / |  ,   /  `---'.|`--''       
            '---"       `----'   ---`-'     `---`            

    ''')
    pass


def set_cookie():
    try:
        response = requests.get(url_cookie)
    except requests.exceptions.ConnectionError:
        logger.info('连接失败')
        print('连接失败')
        sys.exit()
    print(response.headers.get('Set-Cookie'))
    logger.info(response.headers.get('Set-Cookie'))
    str_cookie = response.headers.get('Set-Cookie')
    Cookie[str_cookie.split(';')[0].split('=')[0]] = str_cookie.split(';')[0].split('=')[1]
    print(Cookie)
    logger.info(Cookie)
    headers[str_cookie.split(';')[0].split('=')[0]] = str_cookie.split(';')[0].split('=')[1]

    pass


def get_verification_code_image():
    # 图片URL
    req = requests.get(url=url_get_verification_code, headers=headers, cookies=Cookie, timeout=30)
    # 使用BytesIO接口
    image = Image.open(BytesIO(req.content))
    fileName = str(uuid.uuid4()) + '.' + image.format.lower()
    print('学校登录验证码名称: ' + fileName)
    with open(fileName, 'wb') as f:
        f.write(req.content)
    return fileName
    pass


def get_verification_code(fileName):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        ApiKey, SecretKey)
    try:
        response = requests.get(host).json().get('access_token')
    except requests.exceptions.ConnectionError:
        print('连接错误')
        sys.exit()
    print('百度access_token: ' + response)
    '''
    通用文字识别
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    file = open(fileName, 'rb')
    img = base64.b64encode(file.read())
    params = {"image": img}
    access_token = response
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    verification_code = response.json().get('words_result')[0].get('words')
    print('验证码: ' + verification_code)
    # 有时可能因为图文识别错误，需要重新识别
    if len(verification_code) != 4:
        verification_code = get_verification_code(get_verification_code_image())
    print('验证码长度为：' + str(len(verification_code)))
    return verification_code
    pass


def encryption_parameters(fileName):
    dataCode = requests.get(url=url_code, headers=headers, cookies=Cookie, timeout=30)
    print('学校登录代码: ' + dataCode.text)
    os.remove(fileName)
    file = 'login.js'
    ctx = execjs.compile(open(file).read())
    params = ctx.call("onSubmint", dataCode.text, user_name, password)
    print(params)
    return params
    pass


def get_cookie(params, verification_code):
    formData = {
        'view': 0,
        'useDogCode': '',
        'encoded': params,
        'RANDOMCODE': verification_code
    }
    response = requests.post(url_login, data=formData, cookies=Cookie, headers=headers, stream=True)
    print('返回头参数：' + str(response.headers))
    pass


def class_schedule():
    url = 'http://jw.nnxy.cn/jsxsd/xskb/xskb_print.do?xnxq01id={}&zc={}'.format(semester, week)
    dataCode = requests.get(url=url, headers=headers, cookies=Cookie, timeout=30)
    print(dataCode.content)
    df = pd.read_excel(io.BytesIO(dataCode.content), header=2)
    df = df.iloc[:12]
    return df
    pass


def pands_unparsed_data(df):
    print('开始解析数据')
    col_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    for i in range(0, len(col_list)):
        df.fillna({col_list[i]: " "}, inplace=True)
        df.replace(" ", "无", inplace=True)
    for i in col_list:
        data_temp = {}
        for j in range(0, len(df[i].tolist()), 2):
            data_temp[df['大节'].tolist()[j]] = df[i].tolist()[j]
        data[i] = data_temp
    print(data)
    data['username'] = user_name
    print('解析数据完成')
    pass


def save_mongdb():
    print('开始保存数据')
    client = pymongo.MongoClient("mongodb://{user_name}:{pass_word}@{host}:{port}".format(
        user_name='mongodb用户名',
        pass_word='mongodb密码',
        host='mongodb地址',
        port='mongodb端口'
    ))
    db = client['class_schedule']
    collection = db['class_schedule']
    result = collection.insert_one(data)
    print('保存数据完成')
    print(result)
    print('该数据id为：' + str(result.inserted_id))
    pass


def main():
    set_cookie()
    fileName = get_verification_code_image()
    verification_code = get_verification_code(fileName)
    params = encryption_parameters(fileName)
    get_cookie(params, verification_code)
    print(headers)
    print('----请等待十秒----')
    time.sleep(10)
    try:
        pands_unparsed_data(class_schedule())
    except Exception as e:
        print(e)
        print('解析数据失败')
        print('十秒后重新获取数据')
        time.sleep(10)
        main()
    save_mongdb()
    pass


if __name__ == '__main__':
    show_logo()
    try:
        main()
    except:
        logger.error('程序出现错误')
        print('程序出现错误')
        pass

