#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: crawl.py
@time: 2019/7/15 15:57
@desc:
'''
import requests
from fake_useragent import UserAgent
import time
from hashlib import md5
import json
import os
import re

if __name__ == "__main__":
    contain = ["保险公司－财产险", "保险公司－人身险", "专业中介公司-代理公司", "专业中介公司－经纪公司", "专业中介公司－公估公司", "保险公司-财产险", "保险公司-人身险",
               "专业中介公司-代理公司", "专业中介公司-经纪公司", "专业中介公司-公估公司", "再保险公司", "外资保险公司代表处"]
    source_dir = r'C:\Users\my\Desktop\SPIDER\20_保险公司\各省机构名录_temp'
    res_dir = r'C:\Users\my\Desktop\SPIDER\20_保险公司\各省机构名录'
    count = 1
    for file in os.listdir(source_dir):
        lines = open(os.path.join(source_dir, file), "r", encoding="utf-8").readlines()
        # with open(os.path.join(res_dir, file), "a", encoding="utf-8") as f:
        for line in lines:
            if any(s in line for s in contain):
                print(count, line.replace("\n", ""))
                count += 1
                with open("res","a",encoding="utf-8") as g:
                    g.write(str(count)+line.replace("\n", "")+"\n")
                #     f.write(line)
                # f.close()
