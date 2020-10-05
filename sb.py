from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv


#Functions defined here:
def get_page():
    chrome.maximize_window()
    chrome.get("https://www.sblizingas.lt/vartojimo-kreditas/kredito-gavimas/")
    path = '//*[@id="kg_calculator"]/a'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath('//*[@id="hideCookie"]').click()
    chrome.find_element_by_xpath(path).click()
    path2 = '//*[@id="kgModal"]/div/div/div/div[1]'
    wdw(chrome, 10).until(ec.visibility_of_element_located((by.XPATH, path2)))

def waiter(temp):
    path = '//*[@id="kg_modal_mi"]'
    wdw(chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

def waiter_50():
    path = '//*[@id="kg_modal_mi"]'
    wdw(chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '--'))

def set_amount(amount):
    sum_field = chrome.find_element_by_xpath('//*[@id="modal_credit_output"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    blank_space = chrome.find_element_by_xpath('//*[@id="kgModal"]/div/div/div/div[1]/p')
    blank_space.click()

def set_term(term):
    sum_field = chrome.find_element_by_xpath('//*[@id="modal_term_output"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    blank_space = chrome.find_element_by_xpath('//*[@id="kgModal"]/div/div/div/div[1]/p')
    blank_space.click()

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML").replace(".", ",")
    return installment

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="kg_modal_pn"]').get_attribute("innerHTML").replace(".", ",")
    return interest

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="kg_modal_bkkmn"]').get_attribute("innerHTML").replace(".", ",")
    return APR

def read_admin():
    admin = chrome.find_element_by_xpath('//*[@id="kg_modal_am"]').get_attribute("innerHTML").replace(".", ",")
    return admin

def write_content(amount, term):
    with open('./sb_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    get_page()
    for term in terms:
        set_term(term)
        temp = chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML")
        for amount in amounts:
            if amount == 500 and term >= 36:
                pass
            else:
                if amount == 50 and temp != "--":
                    set_amount(amount)
                    waiter_50()
                    write_content(amount, term)
                    temp = chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML")
                else:
                    set_amount(amount)
                    waiter(temp)
                    write_content(amount, term)
                    temp = chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML")
    chrome.close()

#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [50, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through SB's data is {total_time} minutes.")
