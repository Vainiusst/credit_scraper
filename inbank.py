from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


#Functions defined here:

def waiter_start():
    # Waits until all the elements are loaded to begin
    path = '//*[@id="loancalculator"]/div[2]/span'
    wdw(chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '100.29 EUR'))

def cookie_monster():
    # Closes the cookies' pop-up
    path = '//*[@id="__layout"]/div/div[2]/div[2]/button[2]'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def temp_maker():
    # Finds, formats and returns the temporary value to be used in the subsequen waiter function
    temp = chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[3]/p[1]').get_attribute(
        "innerHTML")
    temp_line = re.search('mėnesio įmoka - \d+\s*\d*.\d+', temp).group()
    temp_text = re.search('\d+\s*\d*.\d+', temp_line).group()
    return temp_text

def waiter(temp):
    # Waits until the temporary value passed into the function is not shown anymore (the element changes)
    path = '//*[@id="loancalculator"]/div[3]/p[1]'
    wdw(chrome, 10).until_not((ec.text_to_be_present_in_element((by.XPATH, path), temp)))

def set_amount(amount):
    # Sets the desired amount
    sum_field = chrome.find_element_by_xpath('//*[@id="amount"]')
    sum_field.clear()
    sum_field.send_keys(str(amount))
    sum_field.send_keys(u'\ue007')

def terms_selector(term):
    # Selects the desired term from the drop-down
    selector = Select(chrome.find_element_by_id("period"))
    selector.select_by_value(str(term))

def read_installment():
    # Reads and formats the installment to be written to CSV
    installment = chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[2]/span').get_attribute("innerHTML")
    installment_comma = re.search('\d+\.\d+', installment).group().replace(".", ",")
    return installment_comma

def read_interest():
    # Reads and formats the interest to be written to CSV
    interest = chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[3]/p[1]').get_attribute("innerHTML")
    interest_line = re.search('metinė palūkanų norma - \d+\.\d+', interest).group()
    interest_iso = re.search('\d+\.\d+', interest_line).group()
    interest_form = str(round(float(interest_iso)/100, 4)).replace(".", ",")
    return interest_form

def read_APR():
    # Reads and formats the APR to be written to CSV
    APR = chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[3]/p[1]').get_attribute("innerHTML")
    APR_line = re.search('BVKKMN - \d+\.\d+', APR).group()
    APR_iso = re.search('\d+\.\d+', APR_line).group()
    APR_form = str(round(float(APR_iso)/100, 4)).replace(".", ",")
    return APR_form

def write_content(amount, term):
    # Writes content into the CSV file
    with open('./inbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        try:
            installment = read_installment()
        except AttributeError:
            installment = combo + 'resulted as a NoneType, please check manually'
        interest = read_interest()
        APR = read_APR()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR])

def do_erryfin(amounts, terms):
    # Combines all the actions necessary for the program to work into a single function
    chrome.maximize_window()
    chrome.get("https://www.inbank.lt/")
    cookie_monster()
    waiter_start()
    for term in terms:
        terms_selector(term)
        for amount in amounts:
            temp = temp_maker()
            set_amount(amount)
            waiter(temp)
            write_content(amount, term)
    chrome.close()



starting_time = time() # Starting time to check the duration of the program

chrome = webdriver.Chrome() # Initializing the Chrome Web driver

# Amounts and terms to be checked
amounts = [1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [6, 12, 24, 36, 48, 60, 72]

do_erryfin(amounts, terms)

ending_time = time() # Ending time to check the duration of the program
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Inbank's data is {total_time} minutes.")