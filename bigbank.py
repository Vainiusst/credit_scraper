from selenium import webdriver
from time import sleep, time
import csv

starting_time = time()

chrome = webdriver.Chrome()

amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
terms = [6, 12, 24, 36, 48, 60, 72, 84, 96]

def set_amount(amount):
    sum_field = chrome.find_element_by_xpath('//*[@id="page-1125_module-b9c19759_calculator-1127-sum"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    chrome.find_element_by_xpath('//*[@id="calculators"]/div/div/div/div[3]/div[2]/div[2]/div/div/label[2]/span[1]/strong').click()

def set_term(term):
    sum_field = chrome.find_element_by_xpath('//*[@id="page-1125_module-b9c19759_calculator-1127-period"]')
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    chrome.find_element_by_xpath('//*[@id="calculators"]/div/div/div/div[3]/div[2]/div[2]/div/div/label[2]/span[1]/strong').click()

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="calculators"]/div/div/div/div[4]/div[2]/div[2]/div/div/div[3]/div/p[2]/span').get_attribute("innerHTML")
    installment_comma = installment.replace(".", ",")
    # print(installment_comma)
    return installment_comma

def write_content(amount, term):
    with open(r'C:\Users\Vainius\Desktop\Smauglys\credit_scraper\venv\bigbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment])


def do_erryfin(amounts, terms):
    try:
        chrome.maximize_window()
        chrome.get("https://www.bigbank.lt/")
        sleep(5)
        for term in terms:
            set_term(term)
            sleep(1)
            for amount in amounts:
                set_amount(amount)
                sleep(1)
                write_content(amount, term)
                sleep(1)
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
print(f"Time to crunch through Bigbank's data is {total_time} minutes.")