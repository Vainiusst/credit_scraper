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
    # Waits until all the necessary elements load to begin/proceed with the reading of the elements
    path = '//*[@id="calculator-main"]/form/div[2]/button'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))

def set_amount(amount):
    # Sets the desired amount
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
    # Sets the desired term
    sum_field = chrome.find_element_by_id("iMaturity")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    sum_field.send_keys(u'\ue007')

def read_installment():
    # Reads the installment and returns it properly formatted to be written into CSV
    installment = chrome.find_element_by_id("monthlyPay")
    installment_amount = installment.get_attribute("innerHTML")
    return installment_amount

def read_interest():
    # Reads the interest rate and returns it properly formatted to be written into CSV
    interest = chrome.find_element_by_css_selector('#text_SN_INTERESTRATE').get_attribute("innerHTML")
    interest_str = re.search('\d+,\d+', interest).group().replace(",", ".")
    interest_form = str(round(float(interest_str)/100, 4)).replace(".", ",")
    return interest_form

def read_APR():
    # Reads the APR and returns it properly formatted to be written into CSV
    APR = chrome.find_element_by_css_selector('#text_SN_KGN').get_attribute("innerHTML")
    APR_str = re.search('\d+,\d+', APR).group().replace(",", ".")
    APR_form = str(round(float(APR_str)/100, 4)).replace(".", ",")
    return APR_form

def read_admin():
    # Reads the APR and returns it properly formatted to be written into CSV
    admin = chrome.find_element_by_css_selector('#text_SN_PROCESSINGFEE').get_attribute("innerHTML")
    admin_str = re.search('\d+,\d+', admin).group().replace(",", ".")
    admin_form = str(round(float(admin_str) / 100, 4)).replace(".", ",")
    return admin_form

def write_content(amount, term):
    # Writes the content into the CSV file
    with open('./gf_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    # Combines all the actions necessary for the program to work into a single function
    chrome.maximize_window()
    chrome.get("https://kreditasinternetu.gf.lt/#vartojimui")
    waiter()
    for term in terms:
        set_term(term)
        for amount in amounts:
            if amount == 100 and term >= 72:
                pass
                # This company does not issue 100€ for terms longer than 72 months, hence these combos are escaped
            else:
                set_amount(amount)
                waiter()
                write_content(amount, term)
    chrome.close()


starting_time = time() # Starting time to check the duration of the program

chrome = webdriver.Chrome() # Initializing the Chrome Web driver

# Amounts and terms to be checked
amounts = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

do_erryfin(amounts, terms)

ending_time = time() # Ending time to check the duration of the program
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through GF's data is {total_time} minutes.")
