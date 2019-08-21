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


class crawler():
    def __init__(self, base_url, source_dir, res_dir):
        self.base_url = base_url
        self.source_dir = source_dir
        self.res_dir = res_dir
        folder = os.path.exists(res_dir)
        if not folder:
            os.makedirs(res_dir)
        else:
            print("{} is exist".format(res_dir))
        key_data = open("./keys_screat_key", "r", encoding="utf-8").readlines()
        self.keyes = [i.split(";")[0] for i in key_data]
        self.screat_keyes = [i.split(";")[-1].replace("\n", "") for i in key_data]

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
        url = self.base_url.format(self.keyes[0], company_name)
        headers = self.get_headers(self.keyes[0], self.screat_keyes[0])
        res = requests.get(url=url, headers=headers).text
        if json.loads(res)["Status"] == "200":
            print(company_name, "查询成功，有结果")

        elif json.loads(res)["Status"] == "102" or json.loads(res)["Status"] == "112":
            print("该账号已使用完....", self.keyes[0])
            self.keyes.remove(self.keyes[0])
            self.screat_keyes.remove(self.screat_keyes[0])
            url = self.base_url.format(self.keyes[0], company_name)
            headers = self.get_headers(self.keyes[0], self.screat_keyes[0])
            res = requests.get(url=url, headers=headers).text

        elif json.loads(res)["Status"] == "201":
            print(company_name, "查询无结果")
        else:
            print(res)
        return res

    def run(self):
        count = 1
        for file_name in os.listdir(self.source_dir):
            print("===============", file_name, "===============")
            file_path = os.path.join(source_dir, file_name)
            lines = open(file_path, encoding="utf-8").readlines()
            for line in lines:
                company_name = line.strip().split()[0]
                res = self.get_data(company_name)

                if json.loads(res)["Status"] == "200":
                    with open("{}/{:0>3}{}.json".format(self.res_dir, count, company_name), "w", encoding="utf-8") as f:
                        f.write(res)

                    count += 1


if __name__ == "__main__":
    res_dir = "./各省机构_full_bussiness"
    source_dir = "./各省机构名录"
    # base_url = "http://api.qichacha.com/ECIV4/GetFullDetailsByName?key={}&keyWord={}"
    # spider = crawler(base_url, source_dir, res_dir)
    # spider.run()


    count = 1
    company_list = []
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        lines = open(file_path, encoding="utf-8").readlines()
        for line in lines:
            print(count, line.strip())
            count += 1
            company_list.append(line.strip())

        print(len(set(company_list)))
