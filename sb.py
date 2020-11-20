from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv


#Functions defined here:
def cookie_monster():
    # Closes the cookies' pop-up
    cookie_path = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, cookie_path)))
    chrome.find_element_by_xpath(cookie_path).click()

def get_calculator():
    # Opens the page, closes the cookie's pop-up and opens the calculator where the necessary info is shown
    path = '//*[@id="kg_calculator"]/a'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()
    path2 = '//*[@id="kgModal"]/div/div/div/div[1]'
    wdw(chrome, 10).until(ec.visibility_of_element_located((by.XPATH, path2)))

def temporary():
    return chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML")

def waiter(temp):
    # Waits until the element is changed before proceeding to writing
    path = '//*[@id="kg_modal_mi"]'
    wdw(chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

def waiter_small():
    # Waits until certain string is shown before proceeding to writing
    # Used to adapt to the speed of a relatively slow page
    path = '//*[@id="kg_modal_mi"]'
    wdw(chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '--'))

def set_amount(amount):
    # Sets the desired amount
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
    # Sets the desired term
    sum_field = chrome.find_element_by_xpath('//*[@id="modal_term_output"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    blank_space = chrome.find_element_by_xpath('//*[@id="kgModal"]/div/div/div/div[1]/p')
    blank_space.click()

def read_installment():
    # Reads and formats the installment to be written to the CSV
    installment = chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML").replace(".", ",")
    return installment

def read_interest():
    # Reads and formats the interest rate to be written to the CSV
    interest = chrome.find_element_by_xpath('//*[@id="kg_modal_pn"]').get_attribute("innerHTML")
    interest_form = str(round(float(interest)/100, 4)).replace(".", ",")
    return interest_form

def read_APR():
    # Reads and formats the APR to be written to the CSV
    APR = chrome.find_element_by_xpath('//*[@id="kg_modal_bkkmn"]').get_attribute("innerHTML")
    APR_form = str(round(float(APR) / 100, 4)).replace(".", ",")
    return APR_form

def read_admin():
    # Reads and formats the admin fee to be written to the CSV
    admin = chrome.find_element_by_xpath('//*[@id="kg_modal_am"]').get_attribute("innerHTML")
    admin_form = str(round(float(admin) / 100, 4)).replace(".", ",")
    return admin_form

def write_content(amount, term):
    # Writes the content into the CSV file
    with open('./sb_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    # Combines all of the actions necessary for the program to run into a single function
    chrome.maximize_window()
    chrome.get("https://www.sblizingas.lt/vartojimo-kreditas/kredito-gavimas/")
    cookie_monster()
    get_calculator()
    for term in terms:
        set_term(term)
        temp = temporary()
        for amount in amounts:
            if (amount == 100 and term > 12) or (amount == 500 and term > 30):
                pass
                # 100€ and smaller amounts are not issued for terms longer than 12 months, so these combos are escaped
                # Same goes for 500€ and terms exceeding 30 months
            else:
                if amount == 20 and temp != "--":
                    set_amount(amount)
                    waiter_small()
                    with open('./sb_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
                        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(["--", "--", "--"])
                    temp = temporary()
                else:
                    set_amount(amount)
                    waiter(temp)
                    write_content(amount, term)
                    temp = temporary()
    chrome.close()


starting_time = time() # Starting time to check the duration of the program

chrome = webdriver.Chrome() # Initializing the Chrome Web driver

# Amounts and terms to be checked
amounts = [20, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

do_erryfin(amounts, terms)

ending_time = time() # Ending time to check the duration of the program
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through SB's data is {total_time} minutes.")
