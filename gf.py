from selenium import webdriver
from time import sleep, time
from datetime import timedelta
import csv
import re


#Functions defined here:
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
    #print(installment_amount)
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
    try:
        #chrome.maximize_window()
        chrome.get("https://kreditasinternetu.gf.lt/?_ga=2.102102470.679028275.1586548011-1260783365.1586548011#vartojimui")
        for term in terms:
            set_term(term)
            sleep(2)
            for amount in amounts:
                set_amount(amount)
                sleep(2)
                write_content(amount, term)
                sleep(3)
        chrome.close()
    except NameError as err1:
        raise err1
        chrome.close()
    except TypeError as err2:
        raise err2
        chrome.close()


#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through GF's data is {total_time} minutes.")
