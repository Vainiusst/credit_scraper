from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv


class Moki:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
        self.terms = [12, 24, 36, 48, 60, 72]

    def waiter(self):
        """Waits untill all of the necesary elements have changed values before proceeding"""
        path = '/html/body/main/div/div[1]/form/div/div/div[5]/div[2]/span'
        temp = self.chrome.find_element_by_xpath(path).get_attribute('innerHTML')
        wdw(self.chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

    def waiter_start(self):
        """Waits until a specific value is shown in the required element before starting the program"""
        path = '/html/body/main/div/div[1]/form/div/div/div[5]/div[2]/span'
        wdw(self.chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '65.57'))

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        path = '//*[@id="cookie-btns"]/a[1]'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def set_amount(self, amount):
        """Sets the desired amount"""
        sum_field = self.chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[2]/div/div[1]/input")
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(amount))
        self.chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/span[1]").click()

    def set_term(self, term):
        """Sets the desired term"""
        sum_field = self.chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[3]/div/div[1]/input")
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(term))
        self.chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div/span[1]").click()

    def read_installment(self):
        """Reads and formats the installment to be written into the CSV"""
        installment = self.chrome.find_element_by_xpath("/html/body/main/div/div[1]/form/div/div/div[5]/div[2]/span").get_attribute("innerHTML")
        installment_comma = installment.replace(".", ",")
        return installment_comma

    def read_interest(self):
        """Reads and formats the interest rate to be written into the CSV"""
        interest = self.chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[6]/p/span[3]').get_attribute("innerHTML")
        interest_divide = str(round(float(interest[:-2])/100, 4))
        interest_comma = interest_divide.replace(".", ",")
        return interest_comma

    def read_APR(self):
        """Reads and formats the APR to be written into the CSV"""
        APR = self.chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[6]/p/span[6]').get_attribute("innerHTML")
        APR_divide = str(round(float(APR[:-2])/100, 4))
        APR_comma = APR_divide.replace(".", ",")
        return APR_comma

    def read_admin(self):
        """Reads and formats the admin fee to be written into the CSV"""
        admin = self.chrome.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div/div[6]/p/span[5]').get_attribute("innerHTML")
        admin_divide = str(round(float(admin[:-2])/100, 4))
        admin_comma = admin_divide.replace(".", ",")
        return admin_comma

    def write_content(self, amount, term):
        """Writes contents into the CSV file"""
        with open('./moki_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            combo = f'{amount}/{term}'
            installment = self.read_installment()
            interest = self.read_interest()
            APR = self.read_APR()
            admin = self.read_admin()
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment, interest, APR, admin])

    def do_erryfin(self, amounts, terms):
        """Combines all of the actions necessary for the program to run into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://www.mokilizingas.lt/")
        self.waiter_start()
        self.cookie_monster()
        for term in self.terms:
            self.set_term(term)
            self.waiter()
            for amount in self.amounts:
                self.set_amount(amount)
                self.waiter()
                self.write_content(amount, term)
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Mokilizingas' data is {total_time} minutes.")
