from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import time
from datetime import timedelta
import csv


#Functions defined here:
class Bigbank:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
        self.terms = [6, 12, 24, 36, 48, 60, 72, 84, 96]

    def set_amount(self, amount):
        """Sets the desired amount"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="page-931_module-a0541d66_calculator-1127-sum"]')
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(amount))
        self.chrome.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[1]/strong').click()

    def set_term(self, term):
        """Sets the desired term"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="page-931_module-a0541d66_calculator-1127-period"]')
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(term))
        self.chrome.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[1]/strong').click()

    def read_installment(self):
        """Checks the installment amount and returns it properly formatted to be written to CSV"""
        installment = self.chrome.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[2]/span').get_attribute("innerHTML")
        installment_comma = installment.replace(".", ",")
        return installment_comma

    def write_content(self, amount, term):
        """Writes content to the CSV"""
        with open('./bigbank_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            combo = f'{amount}/{term}'
            installment = self.read_installment()
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment])

    def waiter(self):
        """Pauses the actions until necessary elements are loaded"""
        WebDriverWait(self.chrome, 5).until(lambda x: x.find_element_by_xpath('//*[@id="vartojimo-paskolos-skaiciukle"]/div[1]/div/div[2]/div/div/div[3]/div/p[2]/span'))

    def do_erryfin(self, amounts, terms):
        """Combines all the actions to be done into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://www.bigbank.lt/vartojimo-paskola/")
        self.waiter()
        for term in self.terms:
            self.set_term(term)
            self.waiter()
            for amount in self.amounts:
                self.set_amount(amount)
                self.waiter()
                self.write_content(amount, term)
                self.waiter()
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Bigbank's data is {total_time} minutes.")