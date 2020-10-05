from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time, sleep
from datetime import timedelta
import csv


#Functions defined here:

def cookie_monster():
    path = '//*[@id="root"]/div[4]/div/button'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def kill_the_messenger():
    element = chrome.find_element_by_xpath('//*[@id="fb-root"]/div[2]/span/iframe')
    chrome.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """, element)

def set_amount(amount):
    sum_field = chrome.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[1]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/input')
    sum_field.clear()
    sum_field.send_keys(str(amount))
    sum_field.send_keys(u'\ue007')

def set_term(term):
    sum_field = chrome.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[1]/div[1]/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/input')
    sum_field.clear()
    sum_field.send_keys(str(term))
    sum_field.send_keys(u'\ue007')

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]').get_attribute("innerHTML")[:-4]
    return installment

def write_content(amount, term):
    with open('./fjordbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment])

def waiter(temp):
    path = '//*[@id="root"]/div[1]/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]'
    wdw(chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://www.fjordbank.lt/paskolos/vartojimo-paskola")
    cookie_monster()
    kill_the_messenger()
    temp = read_installment()
    for term in terms:
        set_term(term)
        waiter(temp)
        temp = read_installment()
        for amount in amounts:
            set_amount(amount)
            waiter(temp)
            write_content(amount, term)
            temp = read_installment()
    chrome.close()


#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
terms = [12, 24, 36, 48, 60]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Fjordbank's data is {total_time} minutes.")