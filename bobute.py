from selenium import webdriver
from time import sleep, time
from datetime import timedelta
import csv


#Functions defined here:
def set_term(term):
    sum_field = chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[1]/div/div/input')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    empty_space = chrome.find_element_by_xpath('//*[@id="tool-main-loan"]')
    empty_space.click()
    sleep(2)

def set_amount(amount):
    sum_field = chrome.find_element_by_xpath('//*[@id="amount-slider"]/div[1]/div/input')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    empty_space = chrome.find_element_by_xpath('//*[@id="tool-main-loan"]')
    empty_space.click()
    sleep(2)

def open_graph():
    button = chrome.find_element_by_xpath('//*[@id="calc-schedule-button"]')
    button.click()
    sleep(1)

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[4]/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    print(APR)
    return APR

def read_admin():
    admin = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[7]/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    print(admin)
    return admin

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[3]/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    print(interest)
    return interest

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/p/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    print(installment)
    return installment

def write_content(amount, term):
    with open(r'.\bobute_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])
        sleep(2)

def to_read_and_write(amount, term):
    open_graph()
    write_content(amount, term)
    chrome.execute_script("window.scrollTo(0, 0)")
    sleep(1)

def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://www.bobutespaskola.lt/")
    sleep(3)
    set_amount(100)
    for term in terms:
        set_term(term)
        for amount in amounts:
            if amount == 100 and term in [3, 6, 12, 24]:
                set_amount(amount)
                to_read_and_write(amount, term)
            elif amount == 500 and term in [6, 12, 24, 36]:
                set_amount(amount)
                to_read_and_write(amount, term)
            elif amount in [1000, 2000] and term in [6, 12, 24, 36, 48]:
                set_amount(amount)
                to_read_and_write(amount, term)
            else:
                pass
    chrome.close()


#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [100, 500, 1000, 2000]
terms = [3, 6, 12, 24, 36, 48]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Bobute's data is {total_time} minutes.")