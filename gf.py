from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


#Functions defined here:

def waiter():
    path = '//*[@id="calculator-main"]/form/div[2]/button'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))

def set_amount(amount):
    sum_field = chrome.find_element_by_id("dCreditSum")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    sum_field.send_keys(u'\ue007')

def set_term(term):
    sum_field = chrome.find_element_by_id("iMaturity")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    sum_field.send_keys(u'\ue007')

def read_installment():
    installment = chrome.find_element_by_id("monthlyPay")
    installment_amount = installment.get_attribute("innerHTML")
    return installment_amount

def read_interest():
    interest = chrome.find_element_by_css_selector('#text_SN_INTERESTRATE').get_attribute("innerHTML")
    interest_str = re.search('\d+,\d+', interest).group()
    return interest_str

def read_APR():
    APR = chrome.find_element_by_css_selector('#text_SN_KGN').get_attribute("innerHTML")
    APR_str = re.search('\d+,\d+', APR).group()
    return APR_str

def read_admin():
    admin = chrome.find_element_by_css_selector('#text_SN_PROCESSINGFEE').get_attribute("innerHTML")
    admin_str = re.search('\d+,\d+', admin).group()
    return admin_str

def write_content(amount, term):
    with open(r'.\gf_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://kreditasinternetu.gf.lt/#vartojimui")
    waiter()
    for term in terms:
        set_term(term)
        for amount in amounts:
            if amount == 100 and term >= 72:
                pass
            else:
                set_amount(amount)
                waiter()
                write_content(amount, term)
    chrome.close()

#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

# amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
# terms = [72, 84]


do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through GF's data is {total_time} minutes.")
