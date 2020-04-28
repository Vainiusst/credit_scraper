from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import csv
import re

starting_time = time()

chrome = webdriver.Chrome()
chrome.get("https://www.credit24.lt/")
sleep(5)
move = ActionChains(chrome)
slider = chrome.find_element_by_xpath('//*[@id="app-widget"]/div/div[1]/div/div[3]/input')
slider_bar = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/div[1]')
sb_size = slider_bar.size
sb_width = sb_size["width"]

amounts = [-0.183673, 0.0816327, 0.1020403, 0.204082, 0.204082, 0.204082, 0.204082]

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[4]/div/span/div/div')
    installment_iso = installment.get_attribute("innerHTML")[:-1]
    print(installment_iso)
    return installment_iso

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[7]/span/div/div')
    interest_iso = interest.get_attribute("innerHTML")[:-1]
    print(interest_iso)
    return (interest_iso)

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[8]/div/span/div/div')
    APR_iso = APR.get_attribute("innerHTML")[:-1]
    print(APR_iso)
    return APR_iso

def write_content():
    with open(r'.\credit24_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        suma = chrome.find_element_by_xpath('//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div[1]/div/div/div/div/span')
        suma_iso = suma.get_attribute("innerHTML")[:-2]
        combo = f'{suma_iso}/36'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR])

def do_erryfin(amounts):
    for amount in amounts:
        offset = sb_width*amount
        move.drag_and_drop_by_offset(slider, offset, 0).perform()
        sleep(2)
        write_content()
        sleep(2)
    chrome.close()

do_erryfin(amounts)
ending_time = time()
total_time = str((ending_time - starting_time)/60)
print(f"Time to crunch through Credit24's data is {total_time} minutes.")
