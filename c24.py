from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


#Functions defined here:
def waiter():
    path = '//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div[1]/div/div/div/div/span'
    wdw(chrome, 5).until(ec.text_to_be_present_in_element((by.XPATH, path), "500 €"))

def cookie_monster():
    path = '//*[@id="onetrust-accept-btn-handler"]'
    wdw(chrome, 5).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[4]/div/span/div/div')
    installment_iso = installment.get_attribute("innerHTML")[:-1]
    return installment_iso

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[7]/span/div/div')
    interest_iso = interest.get_attribute("innerHTML")[:-1]
    return (interest_iso)

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[8]/div/span/div/div')
    APR_iso = APR.get_attribute("innerHTML")[:-1]
    return APR_iso

def write_content():
    with open(r'.\credit24_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        suma = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[3]/div/div[1]/div/div/div/div/span')
        suma_iso = suma.get_attribute("innerHTML")[:-2]
        combo = f'{suma_iso}/36'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR])

def do_erryfin(amounts):
    chrome.get("https://credit24.lt/lt/n/?utm_expid=.w5tpGC0HQ1C6Wf1F6aQO-g.0&utm_referrer")
    waiter()
    cookie_monster()
    move = ActionChains(chrome)
    slider_bar = chrome.find_element_by_xpath(
        '//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/div[1]')
    sb_size = slider_bar.size
    sb_width = sb_size["width"]
    for amount in amounts:
        offset = sb_width*amount
        move.move_to_element_with_offset(slider_bar, offset, 0).click().perform()
        write_content()
    chrome.close()


#Code starts here
starting_time = time()

chrome = webdriver.Chrome()


amounts = [0, 0.0816327, 0.183673, 0.387755, 0.591837, 0.795918, 1]

do_erryfin(amounts)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Credit24's data is {total_time} minutes.")
