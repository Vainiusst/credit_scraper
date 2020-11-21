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


class Moment:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [0, 0.104, 0.132, 0.25, 0.179, 0.035, 0.036, 0.05, 0.05, 0.05, 0.05, 0.05]
        self.terms = [3, 6, 12, 24, 36, 48, 60]

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        path = '//*[@id="pre_header"]/div/div[2]/input'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def set_amount(self, amount):
        """Sets the desired amount"""
        # Full slider length - 564px
        sb_width = self.chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[1]').size["width"]
        slider = self.chrome.find_element_by_xpath('//*[@id="amount_slider_wrap"]/div/span/div[3]')
        move = ActionChains(self.chrome)
        offset = amount * sb_width
        move.drag_and_drop_by_offset(slider, offset, 0).perform()

    def set_term(self, term):
        """Selects the desired term from the drop-down"""
        selector = Select(self.chrome.find_element_by_xpath('//*[@id="duration"]'))
        selector.select_by_value(str(term))

    def read_installment(self):
        """Reads and formats the installment to be written into the CSV"""
        std_ex = self.chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
        iso_str = re.search('mėnesinė įmoka būtų \d+.*\d*,+\d+ EUR', std_ex).group()
        installment = re.search('\d+.*\d*,+\d+', iso_str).group().replace(".", "")
        return installment

    def read_interest(self):
        """Reads and formats the interest rate to be written into the CSV"""
        std_ex = self.chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
        iso_str = re.search('palūkanos būtų \d+,*\d* %', std_ex).group()
        interest_iso = re.search('\d+,*\d*', iso_str).group().replace(",", ".")
        interest_form = str(round(float(interest_iso)/100, 4)).replace(".", ",")
        return interest_form

    def read_APR(self):
        """Reads and formats the APR to be written into the CSV"""
        std_ex = self.chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
        iso_str = re.search('BVKKMN . \d+,\d+%', std_ex).group()
        APR_iso = re.search('\d+,\d+', iso_str).group().replace(",", ".")
        APR_form = str(round(float(APR_iso)/100, 4)).replace(".", ",")
        return APR_form

    def read_admin(self, amount):
        """Reads and formats the admin fee to be written into the CSV"""
        std_ex = self.chrome.find_element_by_xpath('//*[@id="credit_rates_footnote"]/p[2]').get_attribute("innerHTML")
        iso_str = re.search('ir \d+,\d* Eur/mėn\.', std_ex).group()
        admin_str = re.search('\d+,\d*', iso_str).group()
        if admin_str == '0,00':
            return admin_str
        else:
            admin_perc = float(admin_str.replace(",", "."))/int(amount)
            admin_perc_str = str(round(admin_perc, 4)).replace(".", ",")
            return admin_perc_str

    def suma(self):
        """Finds the actual amount that is set on the page
        as opposed to the one that's been passed down as a parameter
        (sometimes they mismatch)"""
        path = '//*[@id="amount_slider_wrap"]/div/span/div[3]/span/span[2]'
        inner = self.chrome.find_element_by_xpath(path).get_attribute("innerHTML")
        suma = re.search('\d+.\d+ <', inner).group()[:-2]
        if ' ' in suma:
            return suma.replace(' ', '')
        else:
            return suma

    def write_content(self, term):
        """Writes all of the content into the CSV file"""
        with open('./moment_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            sum = self.suma()
            combo = f'{sum}/{term}'
            installment = self.read_installment()
            interest = self.read_interest()
            APR = self.read_APR()
            admin = self.read_admin(sum)
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment, interest, APR, admin])


    def do_erryfin(self, amounts, terms):
        """Combines all of the actions necessary for the program to work into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://www.momentcredit.lt")
        self.cookie_monster()
        for term in self.terms:
            self.set_term(term)
            # The page applies logic and obstructs setting of certain combos
            # Thus logo has to be appliedhere too, to avoid crashes
            if term == 3:
                self.set_amount(-0.487) #274.668
                for amount in self.amounts:
                    self.set_amount(amount)
                    self.write_content(term)
            elif term in [6, 12, 24]:
                self.set_amount(-0.987) #556.668
                for amount in self.amounts:
                    self.set_amount(amount)
                    self.write_content(term)
            elif term == 36:
                self.set_amount(-0.75) #423
                self.write_content(term)
                for amount in self.amounts[3:]:
                    self.set_amount(amount)
                    self.write_content(term)
            else:
                self.set_amount(-0.5) #282
                self.write_content(term)
                for amount in self.amounts[4:]:
                    self.set_amount(amount)
                    self.write_content(term)
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Moment Credit's data is {total_time} minutes.")

Moment().main()