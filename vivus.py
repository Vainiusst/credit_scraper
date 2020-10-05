from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv

#Functions defined here:

def cookie_monster():
    path = '//*[@id="page-wrap"]/div[2]/div/div/div[2]/div/div/button'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def set_amount(amount):
    sum_field = chrome.find_element_by_xpath('//*[@id="amount"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    sum_field.send_keys(u'\ue007')

def set_term(term):
    term_field = chrome.find_element_by_xpath('//*[@id="term"]')
    term_field.click()
    term_field.send_keys(u'\ue003')
    term_field.send_keys(u'\ue003')
    term_field.send_keys(str(term))
    term_field.send_keys(u'\ue007')

def amt_term_logic(term, limit):
    set_term(term)
    for x in amounts:
        if x >= limit:
            set_amount(x)
            write_content(x, term)
        else:
            pass

def amt_hi_term_logic(term, limit):
    for x in amounts:
        if x >= limit:
            set_amount(x)
            set_term(term)
            write_content(x, term)
        else:
            pass

def waiter():
    path = '//*[@id="calculatorApply"]'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="offerMonthlyPayment"]')
    installment_amount = installment.get_attribute("innerHTML")[:-9]
    amt_fix = installment_amount.replace(".", ",")
    return amt_fix

def read_interest():
    interest = float(chrome.find_element_by_xpath('//*[@id="offerInterestRate"]').get_attribute("innerHTML")[:-7])
    interest_str = str(round((interest/100), 4)).replace(".", ",")
    return interest_str

def read_APR():
    APR = float(chrome.find_element_by_xpath('//*[@id="offerAnnualPercentageRate"]').get_attribute("innerHTML")[:-7])
    APR_str = str(round((APR/100), 4)).replace(".", ",")
    return APR_str

def read_admin():
    admin = float(chrome.find_element_by_xpath('//*[@id="administrativeFee"]').get_attribute("innerHTML")[:-7])
    admin_str = str(round((admin/1200), 4)).replace(".", ",")
    return admin_str

def write_content(amount, term):
    waiter()
    with open('./vivus_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://www.vivus.lt/")
    cookie_monster()
    for y in terms:
        if y == 3:
            for x in amounts:
                if x <= 2000:
                    set_amount(x)
                    set_term(y)
                    write_content(x, y)
                else:
                    pass
        elif y == 6:
            set_term(y)
            for x in amounts:
                if x <= 5000:
                    set_amount(x)
                    write_content(x, y)
                else:
                    pass
        elif y == 48:
            amt_term_logic(y, 500)
        elif y == 60:
            amt_term_logic(y, 2000)
        elif y >= 72:
            amt_hi_term_logic(y, 5000)
        else:
            set_term(y)
            for x in amounts:
                set_amount(x)
                write_content(x, y)
    chrome.close()



#Code starts here:

starting_time = time()

chrome = webdriver.Chrome()

amounts = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Vivus' data is {total_time} minutes.")
