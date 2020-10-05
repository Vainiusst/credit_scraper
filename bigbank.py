from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import time
from datetime import timedelta
import csv


#Functions defined here:
def set_amount(amount):
    sum_field = chrome.find_element_by_xpath('//*[@id="page-931_module-a0541d66_calculator-1127-sum"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    chrome.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[1]/strong').click()

def set_term(term):
    sum_field = chrome.find_element_by_xpath('//*[@id="page-931_module-a0541d66_calculator-1127-period"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    chrome.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[1]/strong').click()

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[2]/span').get_attribute("innerHTML")
    installment_comma = installment.replace(".", ",")
    # print(installment_comma)
    return installment_comma

def write_content(amount, term):
    with open('./bigbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment])

def waiter():
    WebDriverWait(chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[2]/span'))


def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://www.bigbank.lt/vartojimo-paskola/")
    waiter()
    for term in terms:
        set_term(term)
        waiter()
        for amount in amounts:
            set_amount(amount)
            waiter()
            write_content(amount, term)
            waiter()
    chrome.close()


#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [6, 12, 24, 36, 48, 60, 72, 84, 96]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Bigbank's data is {total_time} minutes.")