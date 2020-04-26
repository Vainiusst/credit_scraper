from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import csv
import re

starting_time = time()

chrome = webdriver.Chrome()

#offsets (pixels), that set the slider at the correct position for the necessary amount/term

amounts= [-543, 108.6, 108.6, 108.6, 108.6, 54.3, 54.3]

terms = [-155.14, 77.59, 77.59, 77.59, 77.59, 77.59, 77.59, 77.59]

def start_up():
    chrome.get("https://www.smspinigai.lt")
    nuolatinis = chrome.find_element_by_xpath('/html/body/div[1]/div[1]/main/section/div/div[2]/div/ul/li[2]')
    nuolatinis.click()

def set_amount(amount):
    slider = chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div/div[1]')
    move_amt = ActionChains(chrome)
    move_amt.click_and_hold(slider).move_by_offset(amount, 0).release().perform()

def set_term(term):
    slider = chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[2]/div/div[1]')
    move_term = ActionChains(chrome)
    move_term.click_and_hold(slider).move_by_offset(term, 0).release().perform()

def open_dets():
    dets = chrome.find_element_by_xpath('/html/body/div[1]/div[1]/main/section/div/div[2]/div/div[4]/a')
    dets.click()

def kill_cookies():
    cookies = chrome.find_element_by_xpath('//*[@id="cookie-vue-app"]/div/div/div[2]')
    cookies.click()

def read_installment():
    installment = chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[3]').get_attribute("innerHTML")[:-2]
    inst_str = re.search('\d+,\d+', installment).group()
    print(inst_str)
    return inst_str

def read_interest():
    interest = chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[5]').get_attribute("innerHTML")[:-2]
    int_str = re.search('\d+,\d+', interest).group()
    print(int_str)
    return int_str

def read_APR():
    APR = chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[6]').get_attribute("innerHTML")[:-2]
    APR_str = re.search('\d+,\d+', APR).group()
    print(APR_str)
    return APR_str

def read_admin():
    admin = chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[4]').get_attribute("innerHTML")[:-2]
    admin_str = re.search('\d+,\d+', admin).group()
    return admin_str

def turn_to_proc(func):
    number = func.replace(",", ".")
    number_fl = float(number)
    amount = chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[1]').get_attribute("innerHTML")[:-2]
    amount_fl = float(re.search('\d+,\d+', amount).group().replace(",", "."))
    proc = str((number_fl*100)/amount_fl)
    proc_str = proc.replace(".", ",")
    print(proc_str)
    return proc_str

def to_mths(string):
    if string[2:] == " mėn.":
        return int(string[1])
    else:
        no_yrs = int(string[0])
        return no_yrs*12

def write_content():
    with open(r'.\smspinigai_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
        suma = chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div/div[2]/span/span').get_attribute("innerHTML")[:-2]
        terminas_pre = chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[2]/div/div[2]/span/span').get_attribute("innerHTML")
        terminas = to_mths(terminas_pre)
        combo = f'{suma}/{terminas}'
        installment = read_installment()
        interest = read_interest()
        APR = read_APR()
        admin = turn_to_proc(read_admin())
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([combo, installment, interest, APR, admin])

def close_dets():
    close_bttn = chrome.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/span')
    close_bttn.click()

def do_erryfin(amounts, terms):
    start_up()
    kill_cookies()
    sleep(1)
    for term in terms:
        set_term(term)
        for amount in amounts:
            set_amount(amount)
            sleep(1)
            open_dets()
            sleep(1)
            write_content()
            close_dets()
            sleep(1)
    chrome.close()


do_erryfin(amounts, terms)
ending_time = time()
total_time = str((ending_time - starting_time)/60)
print(f"Time to crunch through Smspinigai data is {total_time} minutes.")