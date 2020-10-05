from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv


#Functions defined here:

def waiter(temp):
    path = '/html/body/main/div/div[1]/form/div/div/div[7]/div[2]/span'
    wdw(chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

def waiter_start():
    path = '/html/body/main/div/div[1]/form/div/div/div[7]/div[2]/span'
    wdw(chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '65.57'))

def cookie_monster():
    path = '//*[@id="cookie-btns"]/a[1]'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def set_amount(amount):
    sum_field = chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/div[1]/input")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/span[1]").click()

def set_term(term):
    sum_field = chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[6]/div/div[1]/input")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/span[1]").click()

def read_installment():
    installment = chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[7]/div[2]/span").get_attribute("innerHTML")
    installment_comma = installment.replace(".", ",")
    return installment_comma

def read_interest():
    interest = chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[8]/p/span[3]').get_attribute("innerHTML")
    interest_comma = interest.replace(".", ",")[:-2]
    return interest_comma

def read_APR():
    APR = chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[8]/p/span[6]').get_attribute("innerHTML")
    APR_comma = APR.replace(".", ",")[:-2]
    return APR_comma

def read_admin():
    admin = chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[8]/p/span[5]').get_attribute("innerHTML")
    admin_comma = admin.replace(".", ",")[:-2]
    return admin_comma

def write_content(amount, term):
    with open('./moki_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://www.mokilizingas.lt/")
    waiter_start()
    cookie_monster()
    for term in terms:
        set_term(term)
        for amount in amounts:
            set_amount(amount)
            temp = chrome.find_element_by_xpath(
                '/html/body/main/div/div[1]/form/div/div/div[7]/div[2]/span').get_attribute('innerHTML')
            waiter(temp)
            write_content(amount, term)
    chrome.close()


#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [12, 24, 36, 48, 60, 72]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Mokilizingas' data is {total_time} minutes.")
