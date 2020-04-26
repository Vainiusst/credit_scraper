from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import csv
import re

starting_time = time()

chrome = webdriver.Chrome()

# 7.332,

amounts = [0, 58.656, 74.448, 141, 100.956, 19.74, 20.304, 28.2, 28.2, 28.2, 28.2, 28.2]
terms = [3, 6, 12, 24, 36, 48, 60]

chrome.get("https://www.momentcredit.lt")
sleep(2)

def set_amount(amount):
    #full slider length - 564px
    slider = chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[3]')
    move = ActionChains(chrome)
    move.drag_and_drop_by_offset(slider, amount, 0).perform()

def set_term(term):
    selector = Select(chrome.find_element_by_xpath('//*[@id="duration"]'))
    selector.select_by_value(str(term))
    sleep(2)

def read_installment():
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('mėnesinė įmoka būtų \d+.*\d*,+\d+ EUR', std_ex).group()
    installment = re.search('\d+.*\d*,+\d+', iso_str).group().replace(".", "")
    print(installment)
    return installment

def read_interest():
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('palūkanos būtų \d+,*\d* %', std_ex).group()
    interest = re.search('\d+,*\d*', iso_str).group()
    print(interest)
    return interest

def read_APR():
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('BVKKMN . \d+,\d+%', std_ex).group()
    APR = re.search('\d+,\d+', iso_str).group()
    print(APR)
    return APR

def read_admin():
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('ir \d,*\d* Eur/mėn\.', std_ex).group()
    admin = re.search('\d,*\d*', iso_str).group()
    print(admin)
    return admin

def suma():
    inner = chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[3]/span/span[2]').get_attribute("innerHTML")
    suma = re.search('\d+.\d+ <', inner).group()[:-2]
    if ' ' in suma:
        return suma.replace(' ', '')
    else:
        return suma

def write_content(term):
    with open(r'.\moment_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        sum = suma()
        combo = f'{sum}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])
        sleep(2)


def do_erryfin(amounts, terms):
    for term in terms:
        set_term(term)
        if term == 3:
            set_amount(-274.668)
            for amount in amounts:
                set_amount(amount)
                write_content(term)
        elif term in [6, 12, 24]:
            set_amount(-556.668)
            for amount in amounts:
                set_amount(amount)
                write_content(term)
        elif term == 36:
            set_amount(-423)
            write_content(term)
            for amount in amounts[3:]:
                set_amount(amount)
                write_content(term)
        else:
            set_amount(-282)
            write_content(term)
            for amount in amounts[4:]:
                set_amount(amount)
                write_content(term)
        sleep(1)
    chrome.close()


do_erryfin(amounts, terms)
ending_time = time()
total_time = str((ending_time - starting_time)/60)
print(f"Time to crunch through Moment Credit's data is {total_time} minutes.")