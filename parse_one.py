#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: parse_one.py
@time: 2019/7/29 13:56
@desc:
'''
import requests
from fake_useragent import UserAgent
import time
from hashlib import md5
import json
import os


class parse():
    def __init__(self, key, screat_key, base_url):
        self.key = key
        self.screat_key = screat_key
        self.base_url = base_url

    # 获取时间戳
    def get_time_tup(self):
        time_tup = str(int(time.time()))
        return time_tup

    # md5加密
    def set_md5(self, s):
        new_md5 = md5()
        new_md5.update(s.encode(encoding='utf-8'))
        s_md5 = new_md5.hexdigest().upper()
        return s_md5

    # 设置请求头
    def get_headers(self, key, screat_key):
        headers = dict()
        token = key + self.get_time_tup() + screat_key
        headers["Token"] = self.set_md5(token)
        headers["Timespan"] = self.get_time_tup()
        return headers

    def get_data(self, company_name):
        url = self.base_url.format(key, company_name)
        headers = self.get_headers(key, screat_key)

        res = requests.get(url=url, headers=headers).text
        print(res)


if __name__ == "__main__":
    key = "f072ebf649a045e09c092be11624af14"
    screat_key = "33A26D4B1DEF399817597D71A0CAFA07"
    base_url = "http://api.qichacha.com/ECIV4/GetFullDetailsByName?key={}&keyWord={}"
    p = parse(key, screat_key, base_url)
    p.get_data("中德安联人寿保险有限公司")
