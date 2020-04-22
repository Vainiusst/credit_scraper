from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import csv
import re

starting_time = time()

chrome = webdriver.Chrome()

amounts = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
terms = [3, 6, 12, 24, 36, 48, 60, 72]

chrome.get("https://www.momentcredit.lt")
sleep(2)

def set_amount(amount):
    '''
    100 = 17,5% sliderio judesio
    '''
    slider = chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[3]')
    move = ActionChains(chrome)
    move.drag_and_drop_by_offset(slider, amount, 0).perform()

def terms_selector(term):
    selector = Select(chrome.find_element_by_xpath('//*[@id="duration"]'))
    selector.select_by_value(str(term))
    sleep(2)

terms_selector(3)
set_amount(50)
