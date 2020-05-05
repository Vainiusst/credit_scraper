from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep, time
from datetime import timedelta
import csv
import re


#Functions defined here:
def set_amount(amount):
    sum_field = chrome.find_element_by_id("amount")
    sum_field.clear()
    sum_field.send_keys(str(amount))
    sum_field.send_keys(u'\ue007')

def terms_selector(term):
    selector = Select(chrome.find_element_by_id("period"))
    selector.select_by_value(str(term))

def read_installment():
    installment = chrome.find_element_by_xpath("//*[@id='loancalculator']/div[1]/div/div[7]/p/span").get_attribute("innerHTML")
    installment_comma = re.search('\d+.\d+', installment).group().replace(".", ",")
    # print(installment_comma)
    return installment_comma

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[2]/p[1]').get_attribute("innerHTML")
    interest_line = re.search('metinė palūkanų norma - \d+.\d+', interest).group()
    interest_comma = re.search('\d+.\d+', interest_line).group().replace(".", ",")
    # print(interest_comma)
    return interest_comma

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[2]/p[1]').get_attribute("innerHTML")
    APR_line = re.search('BVKKMN - \d+.\d+', APR).group()
    APR_comma = re.search('\d+.\d+', APR_line).group().replace(".", ",")
    # print(APR_comma)
    return APR_comma

def write_content(amount, term):
    with open(r'.\inbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR])

def do_erryfin(amounts, terms):
    try:
        chrome.get("https://www.inbank.lt/")
        sleep(5)
        for term in terms:
            terms_selector(term)
            for amount in amounts:
                set_amount(amount)
                sleep(2)
                write_content(amount, term)
                sleep(2)
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

amounts = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
terms = [6, 12, 24, 36, 48, 60, 72]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Inbank's data is {total_time} minutes.")
