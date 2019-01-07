from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from faker import Faker
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import faker.providers as providers
from random import randint
import random
from tkinter import Tk 
import re
from decimal import Decimal
import email
import imaplib
from bs4 import BeautifulSoup as BS
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import pyperclip
from random import choice
from datetime import datetime
from re import sub

def send(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  if response['status']:
    raise Exception(response.get('value'))
  return response.get('value')

def add_script(driver, script):
  send(driver, "Page.addScriptToEvaluateOnNewDocument", {"source": script})

def getIP():
    r = requests.get('https://ipinfo.io/ip',timeout=3)
    return r.text

def next_available_row(worksheet):
    str_list = list(filter(None, sheet.col_values(1)))  # fastest
    return str(len(str_list)+1)

scriptjs=""
with open('script.js', 'r') as myfile:
  scriptjs= myfile.read()
WebDriver.add_script = add_script

with open(("accounts.txt")) as f: #first line-password, next lines - emails
    line = f.readlines()
emails = [x.strip() for x in line] 
password=emails[0]
email=emails[1] #currently one email supported

print("email: "+str(email))
print("password: "+str(password))
IP=getIP()
print("IP: "+ str(IP[:-1]))


timeout = 10

# launch Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('log-level=3')

driver = webdriver.Chrome(options=chrome_options)


# add a script which will be executed when the page starts loading -> makes selenium harder to detect
driver.add_script(scriptjs)

driver.get("https://trade.aliexpress.com/orderList.htm")

time.sleep(1)
action  = ActionChains(driver)
action = action.send_keys(Keys.TAB *3)
action = action.send_keys(email)
action = action.send_keys(Keys.TAB)
action = action.send_keys(password)
action = action.send_keys(Keys.ENTER)
action.perform()

time.sleep(2)
if("passport" not in str(driver.current_url)):
    print (driver.current_url)
    driver.find_element_by_class_name("button-confirmOrderReceived").click()
    driver.find_element_by_id("select-all").click()
    time.sleep(0.2)
    driver.find_element_by_id("button-confirmOrderReceived").click()
    
    try:
        element_present = EC.presence_of_element_located((By.ID, 'confirm_cpf'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("error")
    driver.find_element_by_id("confirm_cpf").click()
    feedbackStars=driver.find_elements_by_class_name("star-5")
    feedbackStars[0].click()
    feedbackStars[1].click()
    feedbackStars[2].click()
    time.sleep(0.3)
    driver.find_element_by_class_name("ui-textfield-system").send_keys("This is good product!")
    time.sleep(0.3)
    driver.find_element_by_id("buyerLeavefb-submit-btn").click()
    feedbackStatus=driver.find_element_by_class_name("ui-feedback-header").text
    print(feedbackStatus)

else:
    print("Account needs to be verifyied")
