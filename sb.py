from selenium import webdriver
from time import sleep, time
import csv

starting_time = time()

chrome = webdriver.Chrome()

amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

def get_page():
    chrome.maximize_window()
    chrome.get("https://www.sblizingas.lt/vartojimo-kreditas/kredito-gavimas/")
    sleep(2)
    cookies = chrome.find_element_by_xpath('//*[@id="hideCookie"]')
    cookies.click()
    good_button = chrome.find_element_by_xpath('//*[@id="kg_calculator"]/a')
    good_button.click()

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
    # print(installment)
    return installment

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="kg_modal_pn"]').get_attribute("innerHTML").replace(".", ",")
    # print(interest)
    return interest

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="kg_modal_bkkmn"]').get_attribute("innerHTML").replace(".", ",")
    # print(APR)
    return APR

def read_admin():
    admin = chrome.find_element_by_xpath('//*[@id="kg_modal_am"]').get_attribute("innerHTML").replace(".", ",")
    # print(admin)
    return admin

def write_content(amount, term):
    with open(r'.\sb_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def do_erryfin(amounts, terms):
    try:
        get_page()
        sleep(5)
        for term in terms:
            set_term(term)
            for amount in amounts:
                set_amount(amount)
                sleep(1)
                write_content(amount, term)
                sleep(2)
        chrome.close()
    except NameError as err1:
        raise err1
        chrome.close()
    except TypeError as err2:
        raise err2
        chrome.close()

do_erryfin(amounts, terms)
ending_time = time()
total_time = str((ending_time - starting_time)/60)
print(f"Time to crunch through SB's data is {total_time} minutes.")
