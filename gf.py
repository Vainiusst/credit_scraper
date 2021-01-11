from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


class GF:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000, 15000, 20000, 25000]
        self.terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

    def waiter(self):
        """Waits until all the necessary elements load to begin/proceed with the reading of the elements"""
        path = '//*[@id="calculator-main"]/form/div[2]/button'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))

    def set_amount(self, amount):
        """Sets the desired amount"""
        sum_field = self.chrome.find_element_by_id("dCreditSum")
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
        sum_field = self.chrome.find_element_by_id("iMaturity")
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(term))
        sum_field.send_keys(u'\ue007')

    def read_installment(self):
        """Reads the installment and returns it properly formatted to be written into CSV"""
        installment = self.chrome.find_element_by_id("monthlyPay")
        installment_amount = installment.get_attribute("innerHTML")
        return installment_amount

    def read_interest(self):
        """Reads the interest rate and returns it properly formatted to be written into CSV"""
        interest = self.chrome.find_element_by_css_selector('#text_SN_INTERESTRATE').get_attribute("innerHTML")
        interest_str = re.search('\d+,\d+', interest).group().replace(",", ".")
        interest_form = str(round(float(interest_str)/100, 4)).replace(".", ",")
        return interest_form

    def read_APR(self):
        """Reads the APR and returns it properly formatted to be written into CSV"""
        APR = self.chrome.find_element_by_css_selector('#text_SN_KGN').get_attribute("innerHTML")
        APR_str = re.search('\d+,\d+', APR).group().replace(",", ".")
        APR_form = str(round(float(APR_str)/100, 4)).replace(".", ",")
        return APR_form

    def read_admin(self):
        """Reads the APR and returns it properly formatted to be written into CSV"""
        admin = self.chrome.find_element_by_css_selector('#text_SN_PROCESSINGFEE').get_attribute("innerHTML")
        admin_str = re.search('\d+,\d+', admin).group().replace(",", ".")
        admin_form = str(round(float(admin_str) / 100, 4)).replace(".", ",")
        return admin_form

    def read_contract(self, term):
        """Reads the contract fee and returns it properly formatted to be written into CSV"""
        contract = self.chrome.find_element_by_css_selector('#text_SN_SERVICEFEE').get_attribute("innerHTML")
        contract_str = re.search('\d+,\d+', contract).group().replace(",", ".")
        contract_corr = float(contract_str)/term
        contract_form = str(round(contract_corr, 4)).replace(".", ",")
        return contract_form

    def write_content(self, amount, term):
        """Writes the content into the CSV file"""
        with open('./gf_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            combo = f'{amount}/{term}'
            installment = self.read_installment()
            interest = self.read_interest()
            APR = self.read_APR()
            admin = self.read_admin()
            contract = self.read_contract(term)
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment, interest, APR, admin, contract])

    def do_erryfin(self, amounts, terms):
        """Combines all the actions necessary for the program to work into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://kreditasinternetu.gf.lt/#vartojimui")
        self.waiter()
        for term in self.terms:
            self.set_term(term)
            for amount in self.amounts:
                if amount == 100 and term >= 48:
                    pass
                    # This company does not issue 100€ for terms longer than 48 months, hence these combos are escaped
                elif amount < 3000 and term >= 60:
                    pass
                elif amount < 5000 and term >= 72:
                    pass
                elif amount < 8000 and term >= 84:
                    pass
                else:
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
        print(f"Time to crunch through GF's data is {total_time} minutes.")