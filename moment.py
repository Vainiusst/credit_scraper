from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


#Functions defined here:

def cookie_monster():
    # Closes the cookies' pop-up
    path = '//*[@id="pre_header"]/div/div[2]/input'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def set_amount(amount):
    # Sets the desired amount
    # Full slider length - 564px
    sb_width = chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[1]').size["width"]
    slider = chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[3]')
    move = ActionChains(chrome)
    offset = amount * sb_width
    move.drag_and_drop_by_offset(slider, offset, 0).perform()

def set_term(term):
    # Selects the desired term from the drop-down
    selector = Select(chrome.find_element_by_xpath('//*[@id="duration"]'))
    selector.select_by_value(str(term))

def read_installment():
    # Reads and formats the installment to be written into the CSV
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('mėnesinė įmoka būtų \d+.*\d*,+\d+ EUR', std_ex).group()
    installment = re.search('\d+.*\d*,+\d+', iso_str).group().replace(".", "")
    return installment

def read_interest():
    # Reads and formats the interest rate to be written into the CSV
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('palūkanos būtų \d+,*\d* %', std_ex).group()
    interest_iso = re.search('\d+,*\d*', iso_str).group().replace(",", ".")
    interest_form = str(round(float(interest_iso)/100, 4)).replace(".", ",")
    return interest_form

def read_APR():
    # Reads and formats the APR to be written into the CSV
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('BVKKMN . \d+,\d+%', std_ex).group()
    APR_iso = re.search('\d+,\d+', iso_str).group().replace(",", ".")
    APR_form = str(round(float(APR_iso)/100, 4)).replace(".", ",")
    return APR_form

def read_admin(amount):
    # Reads and formats the admin fee to be written into the CSV
    std_ex = chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
    iso_str = re.search('ir \d+,\d* Eur/mėn\.', std_ex).group()
    admin_str = re.search('\d+,\d*', iso_str).group()
    if admin_str == '0,00':
        return admin_str
    else:
        admin_perc = float(admin_str.replace(",", "."))/int(amount)
        admin_perc_str = str(round(admin_perc, 4)).replace(".", ",")
        return admin_perc_str

def suma():
    # Finds the actual amount that is set on the page as opposed to the one that's been passed down as a parameter (sometimes they mismatch)
    inner = chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[3]/span/span[2]').get_attribute("innerHTML")
    suma = re.search('\d+.\d+ <', inner).group()[:-2]
    if ' ' in suma:
        return suma.replace(' ', '')
    else:
        return suma

def write_content(term):
    # Writes all of the content into the CSV file
    with open('./moment_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        sum = suma()
        combo = f'{sum}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin(sum)
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])


def do_erryfin(amounts, terms):
    # Combines all of the actions necessary for the program to work into a single function
    chrome.maximize_window()
    chrome.get("https://www.momentcredit.lt")
    cookie_monster()
    for term in terms:
        set_term(term)
        # The page applies logic and obstructs setting of certain combos
        # Thus logo has to be appliedhere too, to avoid crashes
        if term == 3:
            set_amount(-0.487) #274.668
            for amount in amounts:
                set_amount(amount)
                write_content(term)
        elif term in [6, 12, 24]:
            set_amount(-0.987) #556.668
            for amount in amounts:
                set_amount(amount)
                write_content(term)
        elif term == 36:
            set_amount(-0.75) #423
            write_content(term)
            for amount in amounts[3:]:
                set_amount(amount)
                write_content(term)
        else:
            set_amount(-0.5) #282
            write_content(term)
            for amount in amounts[4:]:
                set_amount(amount)
                write_content(term)
    chrome.close()


starting_time = time() # Starting time to check the duration of the program

chrome = webdriver.Chrome() # Initializing the Chrome Web driver

# Amounts, as offsets for the slider, and terms to be checked
amounts = [0, 0.104, 0.132, 0.25, 0.179, 0.035, 0.036, 0.05, 0.05, 0.05, 0.05, 0.05]
terms = [3, 6, 12, 24, 36, 48, 60]

do_erryfin(amounts, terms)

ending_time = time() # Ending time to check the duration of the program
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Moment Credit's data is {total_time} minutes.")