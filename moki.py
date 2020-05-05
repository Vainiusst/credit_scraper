from selenium import webdriver
from time import sleep, time
from datetime import timedelta
import csv


#Functions defined here:
def set_amount(amount):
    sum_field = chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/div[1]/input")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(amount))
    chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/span[1]").click()

def set_term(term):
    sum_field = chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[6]/div/div[1]/input")
    sum_field.click()
    sum_field.send_keys(u'\ue003')
    sum_field.send_keys(u'\ue017')
    sum_field.send_keys(str(term))
    chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/span[1]").click()

def read_installment():
    installment = chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[7]/div[2]/span").get_attribute("innerHTML")
    installment_comma = installment.replace(".", ",")
    # print(installment_comma)
    return installment_comma

def read_interest():
    interest = chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[8]/p/span[3]').get_attribute("innerHTML")
    interest_comma = interest.replace(".", ",")[:-2]
    # print(interest_comma)
    return interest_comma

def read_APR():
    APR = chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[8]/p/span[6]').get_attribute("innerHTML")
    APR_comma = APR.replace(".", ",")[:-2]
    # print(APR_comma)
    return APR_comma

def read_admin():
    admin = chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[8]/p/span[5]').get_attribute("innerHTML")
    admin_comma = admin.replace(".", ",")[:-2]
    # print(APR_comma)
    return admin_comma

def write_content(amount, term):
    with open(r'.\moki_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        combo = f'{amount}/{term}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = read_admin()
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])


def do_erryfin(amounts, terms):
    try:
        chrome.get("https://www.mokilizingas.lt/")
        sleep(5)
        for term in terms:
            set_term(term)
            sleep(2)
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

amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
terms = [12, 24, 36, 48, 60, 72]

do_erryfin(amounts, terms)

ending_time = time()
total_time = str(timedelta(seconds=ending_time - starting_time))
print(f"Time to crunch through Mokilizingas' data is {total_time} minutes.")
