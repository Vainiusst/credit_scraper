from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementClickInterceptedException
from time import time
from datetime import timedelta
import csv
import re


class Tfbank:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        self.terms = [12, 24, 36, 48, 60, 72]

    def cookie_monster(self):
        """Closes the cookies' pop-up.
        Since the pop-up disappears slowly after clicking "Accept", it is faster to remove the element.
        Otherwise ElementClickInterceptedException is raised."""
        element = self.chrome.find_element_by_xpath('/html/body/div[3]')
        self.chrome.execute_script("""
                                var element = arguments[0];
                                element.parentNode.removeChild(element);
                                """, element)

    def waiter(self):
        """Waits until the element appears on the page"""
        wdw(self.chrome, 10).until(ec.visibility_of_element_located((by.XPATH, '//*[@id="root"]/div/div')))

    def set_amount(self, amount):
        """Sets the desired amount"""
        path = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div[2]/div/input'
        sum_field = self.chrome.find_element_by_xpath(path)
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(amount))
        sum_field.send_keys(u'\ue007')

    def set_term(self, term):
        """Sets the desired term"""
        path = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div/input'
        sum_field = self.chrome.find_element_by_xpath(path)
        sum_field.click()
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(term))
        sum_field.send_keys(u'\ue007')

    def read_installment(self):
        """Reads and formats the installment to be written into the CSV"""
        path = '//*[@id="root"]/div/div/div[1]/div/div/div/div/div[4]/div/div[1]/div[2]/div'
        amount = self.chrome.find_element_by_xpath(path).get_attribute("innerHTML").replace("&nbsp;", "")[:-1]
        return amount

    def write_content(self, amount, term):
        """Writes the contents into the CSV file"""
        with open('./tfbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            combo = f'{amount}/{term}'
            installment = self.read_installment()
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment])


    def do_erryfin(self, amounts, terms):
        """Combines all of the actions required for the program to wrok into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://tfbank.lt/vartojimo-paskola/")
        self.cookie_monster()
        self.waiter()
        for term in self.terms:
            self.set_term(term)
            for amount in self.amounts:
                self.set_amount(amount)
                self.write_content(amount, term)
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through TF bank's data is {total_time} minutes.")
