# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
from lxml import etree
import re
import pymysql
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

def main(phone, pwd):
    # login_url = "http://openapi.qichacha.com/Account/Login"
    login_url = "http://openapi.qichacha.com/DataCenter/MyData"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
    # driver = webdriver.Chrome(executable_path="chromedriver")
    driver.get(login_url)
    time.sleep(3)

    name_butt = driver.find_element_by_id("telNumberTxt")
    pwd_butt = driver.find_element_by_id("passwordTxt")
    commit_butt = driver.find_element_by_id("btn")

    actions = ActionChains(driver)
    actions.move_to_element(name_butt)
    actions.click()
    actions.send_keys(phone)
    actions.move_to_element(pwd_butt)
    actions.click()
    actions.send_keys(pwd)
    actions.move_to_element(commit_butt)
    actions.click()
    actions.perform()
    time.sleep(8)

    # cate_selected_href = driver.find_elements_by_class_name("cate_selected")
    # actions.move_to_element(cate_selected_href)
    # actions.click()
    # actions.perform()

    # key_show_butt = driver.find_element_by_id("exchange")
    # screat_key_show_butt = driver.find_element_by_id("exchangeSK")
    # actions.move_to_element(key_show_butt).click()
    # actions.move_to_element(screat_key_show_butt).click()
    # actions.perform()
    # time.sleep(5)


    driver.find_element_by_id("exchange").click()
    driver.find_element_by_id("exchangeSK").click()
    time.sleep(5)

    key = driver.find_element_by_id("spUserKey").text
    screat_key = driver.find_element_by_id("secretKey").text
    print(phone, pwd)
    print(key, "===", screat_key)

    with open("keys_screat_key", "a", encoding="utf-8") as f:
        f.write(key.strip() + ";" + screat_key.strip() + "\n")
        f.close()

    driver.close()


if __name__ == "__main__":
    lines = open("phone_pwd", "r", encoding="utf-8").readlines()
    for line in lines[50:]:
        phone = line.split("----")[0]
        pwd = line.strip().split("----")[-1]
        main(phone, pwd)
