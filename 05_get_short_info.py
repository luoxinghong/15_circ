# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: get_tabid.py
@time: 2019/7/30 9:09
@desc:
'''
import re
import requests
import time
import MySQLdb
import pymysql
import datetime
from xpinyin import Pinyin
import os
import logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

a = '''
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8
Cache-Control:max-age=0
Connection:keep-alive
Cookie:COOKIE_USERID=LTE`; Hm_lvt_6a2f36cc16bd9d0b01b10c2961b8900c=1563242418; __jsluid_h=fa0fe32896e43dba4d53993e003eaded; .ASPXANONYMOUS=VIhqmRx61QEkAAAAYmI2NGViZWQtMTQ4OS00M2FkLTkyZmItZTE4NTJmZmQ4Y2Rh0; ASP.NET_SessionId=yunjrj2nztup1ki3kitxct55; language_49=zh-CN; Hm_lpvt_6a2f36cc16bd9d0b01b10c2961b8900c=1564448428
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36
'''
headers = {i.split(":", 1)[0]: i.split(":")[1] for i in a.split("\n")[1:-1]}


def get_urls(prefix_url, file_path):
    text = open(file_path, encoding="utf-8").read()
    pattern = re.compile("OpenWin\('(.*?)'\)")
    temp_urls = re.findall(pattern, text)

    # print(temp_urls)
    urls = [prefix_url + i for i in temp_urls]
    # print(urls)
    # print(len(urls))

    return urls


def save_to_db(insurance_info):
    conn = MySQLdb.connect("106.12.8.109", "root", "lxh123", "baojian", charset='utf8')
    cursor = conn.cursor()
    sql_str = '''insert into insurance2(Province,Name,Type,StartDate,Address,PhoneNumber,OperName,StockType,Place_of_Registration,Status,Code,Business,Issued_by,Effective_date,Date_of_issue,Certification_authority) values("{Province}","{Name}","{Type}","{StartDate}","{Address}","{PhoneNumber}","{OperName}","{StockType}","{Place_of_Registration}","{Status}","{Code}","{Business}","{Issued_by}","{Effective_date}","{Date_of_issue}","{Certification_authority}")'''
    sql_str = sql_str.format(
        Province=pymysql.escape_string(insurance_info['Province']),
        Name=pymysql.escape_string(insurance_info['Name']),
        Type=pymysql.escape_string(insurance_info['Type']),
        StartDate=insurance_info['StartDate'],
        Address=pymysql.escape_string(insurance_info['Address']),
        PhoneNumber=pymysql.escape_string(insurance_info['PhoneNumber']),
        OperName=pymysql.escape_string(insurance_info['OperName']),
        StockType=pymysql.escape_string(insurance_info['StockType']),
        Place_of_Registration=pymysql.escape_string(insurance_info['Place_of_Registration']),
        Status=pymysql.escape_string(insurance_info['Status']),
        Code=pymysql.escape_string(insurance_info['Code']),
        Business=pymysql.escape_string(insurance_info['Business']),
        Issued_by=pymysql.escape_string(insurance_info['Issued_by']),
        Effective_date=pymysql.escape_string(insurance_info['Effective_date']),
        Date_of_issue=pymysql.escape_string(insurance_info['Date_of_issue']),
        Certification_authority=pymysql.escape_string(insurance_info['Certification_authority'])
    )
    cursor.execute(sql_str)
    conn.commit()
    conn.close()


def parse_url(url):
    html_str = requests.get(url, headers=headers, timeout=15).text.replace("\n", "")
    Name = re.findall('ViewOrganization_lblComName">([\s\S]*?)</span>', html_str)[0].replace("\n", " ")
    print(Name)
    StartDate = re.findall('ViewOrganization_lblOrgDate">(.*?)</span>', html_str)[0]
    Type = re.findall('ViewOrganization_lblComType">(.*?)</span>', html_str)[0]
    print("===", Type)
    Address = re.findall('ViewOrganization_lblAddress">(.*?)</span>', html_str)[0]
    PhoneNumber = re.findall('ViewOrganization_lblTel">(.*?)</span>', html_str)[0]
    OperName = re.findall('ViewOrganization_lblPrincipal">(.*?)</span>', html_str)[0]
    StockType = re.findall('ViewOrganization_lblSW">(.*?)</span>', html_str)[0]
    Place_of_Registration = re.findall('ViewOrganization_lblRegAddress">(.*?)</span>', html_str)[0]
    Status = re.findall('ViewOrganization_lblState">(.*?)</span>', html_str)[0]

    Code = re.findall('ViewOrganization_lblCode">(.*?)</span>', html_str)[0] if len(
        re.findall('ViewOrganization_lblCode">(.*?)</span>', html_str)) > 0 else ""
    Business = re.findall('ViewOrganization_lblBusinessArea">(.*?)</span>', html_str)[0] if len(
        re.findall('ViewOrganization_lblBusinessArea">(.*?)</span>', html_str)) > 0 else ""
    Issued_by = re.findall('ViewOrganization_lblIssuanceAuthority">(.*?)</span>', html_str)[0] if len(
        re.findall('ViewOrganization_lblIssuanceAuthority">(.*?)</span>', html_str)) > 0 else ""
    Effective_date = re.findall('ViewOrganization_lblPeriodOfValidity">(.*?)</span>', html_str)[0] if len(
        re.findall('ViewOrganization_lblPeriodOfValidity">(.*?)</span>', html_str)) > 0 else ""
    Date_of_issue = re.findall('ViewOrganization_lblIssuanceDate">(.*?)</span>', html_str)[0] if len(
        re.findall('ViewOrganization_lblIssuanceDate">(.*?)</span>', html_str)) > 0 else ""
    Certification_authority = re.findall('ViewOrganization_lblProducedAuthority">(.*?)</span>', html_str)[0] if len(
        re.findall('ViewOrganization_lblProducedAuthority">(.*?)</span>', html_str)) > 0 else ""

    insurance_info = {"Name": Name, "StartDate": StartDate, "Address": Address, "PhoneNumber": PhoneNumber,
                      "OperName": OperName, "StockType": StockType, "Place_of_Registration": Place_of_Registration,
                      "Status": Status, "Code": Code, "Business": Business, "Issued_by": Issued_by,
                      "Effective_date": Effective_date, "Date_of_issue": Date_of_issue,
                      "Certification_authority": Certification_authority, "Type": Type}

    return insurance_info


def main():
    # 陕西  shaanxi; 重庆 chongqing; 西藏  xizang  这三个需要单独爬Pinyin无法识别多音字
    for file in os.listdir(r"C:\Users\my\Desktop\SPIDER\20_保险公司\各省HTML"):
        provice_file_path = os.path.join(r"C:\Users\my\Desktop\SPIDER\20_保险公司\各省HTML", file)
        name = file.split(".")[0]
        pin = Pinyin()
        prefix_url = "http://{}.circ.gov.cn/tabid".format(pin.get_pinyin(name).replace("-", ''))
        # prefix_url = "http://chongqing.circ.gov.cn/tabid"
        urls = get_urls(prefix_url, provice_file_path)
        l = len(urls)
        count = 1
        for url in urls:
            print(count, l, url)
            count += 1
            try:
                insurance_info = parse_url(url)
                insurance_info["Province"] = name
                save_to_db(insurance_info)
            except Exception as e:
                logger.info(url)
                logger.info(e)
            continue


if __name__ == "__main__":
    main()
