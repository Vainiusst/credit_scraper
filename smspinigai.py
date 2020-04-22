from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
# import csv
import re

# starting_time = time()

chrome = webdriver.Chrome()

amounts = [500, 1000, 2000, 3000, 4000, 5000]

def start_up():
    chrome.get("https://www.smspinigai.lt")
    nuolatinis = chrome.find_element_by_xpath('/html/body/div[1]/div[1]/main/section/div/div[2]/div/ul/li[2]')
    nuolatinis.click()
    slider = chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div')
    move = ActionChains(chrome)
    move.click_and_hold(slider).move_by_offset(-204, 0).release().perform()
    sleep(0.5)
    slider = chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[2]/div/div[1]')
    move = ActionChains(chrome)
    move.click_and_hold(slider).move_by_offset(-204, 0).release().perform()
    sleep(0.5)

def set_amount(amount):
    plus_button = chrome.find_element_by_xpath('/html/body/div[1]/div[1]/main/section/div/div[1]/div[1]/span[2]')
    int_amount = chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div/div[2]/span/span').get_attribute("innerHTML")[:-2]
    amount_shown = re.search('\d+', int_amount).group()
    while int(amount_shown) < int(amount):
        plus_button.click()
        print(amount_shown)
        sleep(5)
    print(int_amount)
    sleep(2)

start_up()
for amount in amounts:
    set_amount(amount)
chrome.close()