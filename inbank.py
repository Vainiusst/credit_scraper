from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


class Inbank:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
        self.terms = [6, 12, 24, 36, 48, 60, 72]

    def waiter_start(self):
        """Waits until all the elements are loaded to begin"""
        path = '//*[@id="loancalculator"]/div[2]/span'
        wdw(self.chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '100.29 EUR'))

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        path = '//*[@id="__layout"]/div/div[2]/div[2]/button[2]'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def temp_maker(self):
        """Finds, formats and returns the temporary value to be used in the subsequen waiter function"""
        temp = self.chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[3]/p[1]').get_attribute(
            "innerHTML")
        temp_line = re.search('mėnesio įmoka - \d+\s*\d*.\d+', temp).group()
        temp_text = re.search('\d+\s*\d*.\d+', temp_line).group()
        return temp_text

    def waiter(self, temp):
        """Waits until the temporary value passed into the function is not shown anymore (the element changes)"""
        path = '//*[@id="loancalculator"]/div[3]/p[1]'
        wdw(self.chrome, 10).until_not((ec.text_to_be_present_in_element((by.XPATH, path), temp)))

    def set_amount(self, amount):
        """Sets the desired amount"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="amount"]')
        sum_field.clear()
        sum_field.send_keys(str(amount))
        sum_field.send_keys(u'\ue007')

    def terms_selector(self, term):
        """Selects the desired term from the drop-down"""
        selector = Select(self.chrome.find_element_by_id("period"))
        selector.select_by_value(str(term))

    def read_installment(self):
        """Reads and formats the installment to be written to CSV"""
        installment = self.chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[2]/span').get_attribute("innerHTML")
        installment_comma = re.search('\d+\.\d+', installment).group().replace(".", ",")
        return installment_comma

    def read_interest(self):
        """Reads and formats the interest to be written to CSV"""
        interest = self.chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[3]/p[1]').get_attribute("innerHTML")
        interest_line = re.search('metinė palūkanų norma - \d+\.\d+', interest).group()
        interest_iso = re.search('\d+\.\d+', interest_line).group()
        interest_form = str(round(float(interest_iso)/100, 4)).replace(".", ",")
        return interest_form

    def read_APR(self):
        """Reads and formats the APR to be written to CSV"""
        APR = self.chrome.find_element_by_xpath('//*[@id="loancalculator"]/div[3]/p[1]').get_attribute("innerHTML")
        APR_line = re.search('BVKKMN - \d+\.\d+', APR).group()
        APR_iso = re.search('\d+\.\d+', APR_line).group()
        APR_form = str(round(float(APR_iso)/100, 4)).replace(".", ",")
        return APR_form

    def write_content(self, amount, term):
        """Writes content into the CSV file"""
        with open('./inbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            combo = f'{amount}/{term}'
            try:
                installment = self.read_installment()
            except AttributeError:
                installment = combo + 'resulted as a NoneType, please check manually'
            interest = self.read_interest()
            APR = self.read_APR()
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment, interest, APR])

    def do_erryfin(self, amounts, terms):
        """Combines all the actions necessary for the program to work into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://www.inbank.lt/")
        self.cookie_monster()
        self.waiter_start()
        for term in self.terms:
            self.terms_selector(term)
            for amount in self.amounts:
                temp = self.temp_maker()
                self.set_amount(amount)
                self.waiter(temp)
                self.write_content(amount, term)
        self.chrome.close()


    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Inbank's data is {total_time} minutes.")
