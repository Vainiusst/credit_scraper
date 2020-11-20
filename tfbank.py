from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementClickInterceptedException
from time import time
from datetime import timedelta
import csv
import re

def cookie_monster():
    # Closes the cookies' pop-up. Since the pop-up disappears slowly after clicking "Accept", it is faster to remove the element.
    # Otherwise ElementClickInterceptedException is raised.
    element = chrome.find_element_by_xpath('/html/body/div[3]')
    chrome.execute_script("""
                            var element = arguments[0];
                            element.parentNode.removeChild(element);
                            """, element)

def waiter():
    # Waits until the element appears on the page
    wdw(chrome, 10).until(ec.visibility_of_element_located((by.XPATH, '//*[@id="root"]/div/div')))

def set_amount(amount):
    # Sets the desired amount
    path = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/input'
    sum_field = chrome.find_element_by_xpath(path)
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
    # Sets the desired term
    path = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/input'
    sum_field = chrome.find_element_by_xpath(path)
    sum_field.click()
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    sum_field.send_keys(u'\ue007')

def read_installment():
    # Reads and formats the installment to be written into the CSV
    path = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[4]/div/div[1]/div[2]/div'
    amount = chrome.find_element_by_xpath(path).get_attribute("innerHTML").replace("&nbsp;", "")[:-1]
    return amount

def write_content(amount, term):
    # Writes the contents into the CSV file
    with open('./tfbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment])


def do_erryfin(amounts, terms):
    # Combines all of the actions required for the program to wrok into a single function
    chrome.maximize_window()
    chrome.get("https://tfbank.lt/vartojimo-paskola/")
    cookie_monster()
    waiter()
    for term in terms:
        set_term(term)
        for amount in amounts:
            set_amount(amount)
            write_content(amount, term)
    chrome.close()


starting_time = time() # Starting time to check the duration of the program

chrome = webdriver.Chrome() # Initializing the Chrome Web driver

# Amounts and terms to be checked
amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [12, 24, 36, 48, 60, 72]

do_erryfin(amounts, terms)

ending_time = time() # Ending time to check the duration of the program
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through TF bank's data is {total_time} minutes.")