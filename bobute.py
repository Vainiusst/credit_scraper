from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from time import time, sleep
from datetime import timedelta
import csv


#Functions defined here:

def cookie_monster():
    path = '/html/body/div[1]/div/a'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def waiter_start():
    path = '//*[@id="tool-main-loan"]/div[2]/div[3]/span[2]/sup'
    wdw(chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '22 €'))

def kill_the_nav_bar():
    element = chrome.find_element_by_xpath('/html/body/div[6]/nav[1]')
    chrome.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """, element)

def waiter_scroll():
    wdw(chrome, 10).until(ec.visibility_of_element_located((by.XPATH, '//*[@id="bob-calculator-block"]/div/div/ul/li[2]')))

def set_term(term):
    bar_width = chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[2]').size["width"]
    slider = chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[2]/div[2]/div')
    move_term = ActionChains(chrome)
    offset = term * bar_width
    move_term.drag_and_drop_by_offset(slider, offset, 0).perform()

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

def open_graph():
    button = chrome.find_element_by_xpath('//*[@id="calc-schedule-button"]')
    button.click()

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[4]/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    return APR

def read_admin():
    admin = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[7]/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    return admin

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[3]/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    return interest

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/p/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    return installment

def write_content(amount, term):
    with open('./bobute_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def to_read_and_write(amount, term):
    open_graph()
    write_content(amount, term)
    try:
        chrome.execute_script("window.scrollTo(0, 0);")
        waiter_scroll()
    except:
        chrome.execute_script("window.scrollTo(0, 0);")
    sleep(0.75)

def do_erryfin(amounts, terms):
    chrome.maximize_window()
    chrome.get("https://www.bobutespaskola.lt/")
    cookie_monster()
    waiter_start()
    kill_the_nav_bar()
    set_amount(100)
    for term in terms:
        set_term(term)
        for amount in amounts:
            month = int(chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[1]/div/div/input').get_attribute("value"))
            if amount == 100 and month in [3, 6, 12, 24]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount == 500 and month in [6, 12, 24, 36]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount in [1000, 2000] and month in [6, 12, 24, 36, 48]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount in [3000, 4000, 5000] and month in [12, 24, 36, 48]:
                set_amount(amount)
                to_read_and_write(amount, month)
            else:
                pass
    chrome.close()


#Code starts here:
starting_time = time()

chrome = webdriver.Chrome()

amounts = [100, 500, 1000, 2000, 3000, 4000, 5000]
terms = [-1, 0.25, 0.25, 0.5, 0.25, 0.25]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Bobute's data is {total_time} minutes.")
