from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time, sleep
from datetime import timedelta
import csv


class Fjord:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        self.terms = [12, 24, 36, 48, 60]

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        path = '//*[@id="root"]/div[4]/div/button'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    # def kill_the_messenger(self):
    #     """Removes the Messenger window which blocks necessary elements"""
    #     # It appears that the page has removed the Messenger window, but I'll leave the function here for the future, just in case
    #     element = self.chrome.find_element_by_xpath('//*[@id="fb-root"]/div[2]/span/iframe')
    #     self.chrome.execute_script("""
    #                 var element = arguments[0];
    #                 element.parentNode.removeChild(element);
    #                 """, element)

    def set_amount(self, amount):
        """Sets the desired amount"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="Paskolos suma"]')
        sum_field.clear()
        sum_field.send_keys(str(amount))
        sum_field.send_keys(u'\ue007')

    def set_term(self, term):
        """Sets the desired term"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="Laikotarpis"]')
        sum_field.clear()
        sum_field.send_keys(str(term))
        sum_field.send_keys(u'\ue007')

    def read_installment(self):
        """Reads the installment and returns it properly formatted to be written in the CSV"""
        path = '//*[@id="root"]/div[1]/div/div[1]/div[1]/div[3]/div[2]/div[2]/div/div[2]'
        installment = self.chrome.find_element_by_xpath(path).get_attribute("innerHTML")[:-4]
        return installment

    def write_content(self, amount, term):
        """Writes the contents into the CSV"""
        with open('./fjord_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            combo = f'{amount}/{term}'
            installment = self.read_installment()
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment])

    def waiter(self, temp):
        """Waits until the installment amount changes to write the correct data"""
        path = '//*[@id="root"]/div[1]/div/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]'
        wdw(self.chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

    def do_erryfin(self, amounts, terms):
        """Combines all the actions necessary for the program to work into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://www.fjordbank.lt/paskolos/vartojimo-paskola")
        self.cookie_monster()
        #self.kill_the_messenger()
        temp = self.read_installment()
        for term in self.terms:
            self.set_term(term)
            self.waiter(temp)
            temp = self.read_installment()
            for amount in self.amounts:
                self.set_amount(amount)
                self.waiter(temp)
                self.write_content(amount, term)
                temp = self.read_installment()
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Fjordbank's data is {total_time} minutes.")
