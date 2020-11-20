from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from time import time, sleep
from datetime import timedelta
import csv


#Functions defined here:

def cookie_monster():
    # Closes the cookies' pop-up
    path = '/html/body/div[1]/div/a'
    wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
    chrome.find_element_by_xpath(path).click()

def waiter_start():
    # Waits until necessary elements are loaded
    path = '//*[@id="tool-main-loan"]/div[2]/div[3]/span[2]/sup'
    wdw(chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '22 €'))

def kill_the_nav_bar():
    # Removes the navigation bar which often impedes the execution of the program (intercepts the clicks)
    element = chrome.find_element_by_xpath('/html/body/div[6]/nav[1]')
    chrome.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """, element)

def waiter_scroll():
    # Waits for the calculator to appear on the screen after a scroll to the top
    wdw(chrome, 10).until(ec.visibility_of_element_located((by.XPATH, '//*[@id="bob-calculator-block"]/div/div/ul/li[2]')))

def set_term(width, term):
    # Sets the desired term
    try:
        slider = chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[2]/div[2]/div')
        move_term = ActionChains(chrome)
        offset = term * width
        move_term.drag_and_drop_by_offset(slider, offset, 0).perform()
    except StaleElementReferenceException:
        # This exception often comes up when the scrolling to the top fails for some reason, thus we need to retry
        waiter_scroll()
        set_term(width, term)

def set_amount(amount):
    # Sets the desired amount
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
    # Opens the details for the payment
    button = chrome.find_element_by_xpath('//*[@id="calc-schedule-button"]')
    button.click()

def read_APR():
    # Reads the APR and returns it properly formatted to be written to CSV
    APR_raw = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[4]/span').get_attribute("innerHTML")[:-1]
    APR_form = str(round(float(APR_raw)/100, 4)).replace(".", ",")
    return APR_form

def read_admin():
    # Reads the admin fee and returns it properly formatted to be written to CSV
    admin_raw = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[7]/span').get_attribute("innerHTML")[:-1]
    admin_form = str(round(float(admin_raw) / 100, 4)).replace(".", ",")
    return admin_form

def read_interest():
    # Reads the interest and returns it properly formatted to be written to CSV
    interest_raw = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/div/p[3]/span').get_attribute("innerHTML")[:-1]
    interest_form = str(round(float(interest_raw) / 100, 4)).replace(".", ",")
    return interest_form

def read_installment():
    # Reads the installment and returns it properly formatted to be written to CSV
    installment = chrome.find_element_by_xpath('//*[@id="payment-table"]/div[2]/div/div/div[3]/div/p/span').get_attribute("innerHTML").replace(".", ",")[:-1]
    return installment

def write_content(amount, term):
    # Writes the content into the CSV file
    with open('./bobute_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def to_read_and_write(amount, term):
    # Combines all the necessary actions to read the information ad write it into the CSV file
    open_graph()
    write_content(amount, term)
    # Scrolling does not always work smoothly on this page hence, some try-except blocks are necessary
    try:
        chrome.execute_script("window.scrollTo(0, 0);")
        waiter_scroll()
    except:
        chrome.execute_script("window.scrollTo(0, 0);")
    sleep(0.75) # Sleep is necessary to make things slower, otherwise the page seems to crash


def do_erryfin(amounts, terms):
    # Combines all the necessary actions for the program to run
    chrome.maximize_window()
    chrome.get("https://www.bobutespaskola.lt/")
    cookie_monster()
    #waiter_start()
    kill_the_nav_bar()
    bar_width = chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[2]').size["width"]
    set_amount(100)
    for term in terms:
        set_term(bar_width, term)
        for amount in amounts:
            month = int(chrome.find_element_by_xpath('//*[@id="durations-slider"]/div[1]/div/div/input').get_attribute("value"))
            # This page uses a relatively complex logic for their amount/term combinations - they must be selected carefully
            if amount == 100 and month in [3, 6, 12, 24]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount == 500 and month in [6, 12, 24, 36]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount == 1000 and month in [6, 12, 24, 36, 48]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount in [2000, 3000, 4000] and month in [12, 24, 36, 48, 60]:
                set_amount(amount)
                to_read_and_write(amount, month)
            elif amount == 5000 and month in [12, 24, 36, 48, 60, 72]:
                set_amount(amount)
                to_read_and_write(amount, month)
            else:
                pass
    chrome.close()


starting_time = time() # Starting time to check the duration of the program

chrome = webdriver.Chrome() # Initializing the Chrome Web driver

# Amounts and terms to be checked
amounts = [100, 500, 1000, 2000, 3000, 4000, 5000]
# Terms are determined by the slider (offsets) because the input field seems to behave eratically when used at high speeds
terms = [-1, 0.25, 0.25, 0.3333, 0.1667, 0.1667, 0.1667, 0.1667]

do_erryfin(amounts, terms)

ending_time = time() # Ending time to check the duration of the program
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Bobute's data is {total_time} minutes.")