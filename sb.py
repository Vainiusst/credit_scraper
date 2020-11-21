from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from time import time
from datetime import timedelta
import csv


class SB:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [20, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000]
        self.terms = [3, 6, 12, 24, 36, 48, 60, 72, 84]

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        cookie_path = '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, cookie_path)))
        self.chrome.find_element_by_xpath(cookie_path).click()

    def get_calculator(self):
        """Opens the page, closes the cookie's pop-up and opens the calculator where the necessary info is shown"""
        chrome = self.chrome
        path = '//*[@id="kg_calculator"]/a'
        wdw(chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        chrome.find_element_by_xpath(path).click()
        path2 = '//*[@id="kgModal"]/div/div/div/div[1]'
        wdw(chrome, 10).until(ec.visibility_of_element_located((by.XPATH, path2)))

    def temporary(self):
        """Sets a temporary value required for the waiter method"""
        return self.chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML")

    def waiter(self, temp):
        """Waits until the element is changed before proceeding to writing"""
        path = '//*[@id="kg_modal_mi"]'
        wdw(self.chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

    def waiter_small(self):
        """Waits until certain string is shown before proceeding to writing.
        Used to adapt to the speed of a relatively slow page"""
        # Sometimes the amount is set incorrectly and results in TimeoutException
        # Then, we should reset the amount to 20 and try again
        try:
            path = '//*[@id="kg_modal_mi"]'
            wdw(self.chrome, 10).until(ec.text_to_be_present_in_element((by.XPATH, path), '--'))
        except TimeoutException:
            self.set_amount(20)
            self.waiter_small()

    def set_amount(self, amount):
        """Sets the desired amount"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="modal_credit_output"]')
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(amount))
        blank_space = self.chrome.find_element_by_xpath('//*[@id="kgModal"]/div/div/div/div[1]/p')
        blank_space.click()

    def set_term(self, term):
        """Sets the desired term"""
        sum_field = self.chrome.find_element_by_xpath('//*[@id="modal_term_output"]')
        sum_field.click()
        sum_field.send_keys(u'\ue003')
        sum_field.send_keys(u'\ue017')
        sum_field.send_keys(str(term))
        blank_space = self.chrome.find_element_by_xpath('//*[@id="kgModal"]/div/div/div/div[1]/p')
        blank_space.click()

    def read_installment(self):
        """Reads and formats the installment to be written to the CSV"""
        installment = self.chrome.find_element_by_xpath('//*[@id="kg_modal_mi"]').get_attribute("innerHTML").replace(".", ",")
        return installment

    def read_interest(self):
        """Reads and formats the interest rate to be written to the CSV"""
        interest = self.chrome.find_element_by_xpath('//*[@id="kg_modal_pn"]').get_attribute("innerHTML")
        interest_form = str(round(float(interest)/100, 4)).replace(".", ",")
        return interest_form

    def read_APR(self):
        """Reads and formats the APR to be written to the CSV"""
        APR = self.chrome.find_element_by_xpath('//*[@id="kg_modal_bkkmn"]').get_attribute("innerHTML")
        APR_form = str(round(float(APR) / 100, 4)).replace(".", ",")
        return APR_form

    def read_admin(self):
        """Reads and formats the admin fee to be written to the CSV"""
        admin = self.chrome.find_element_by_xpath('//*[@id="kg_modal_am"]').get_attribute("innerHTML")
        admin_form = str(round(float(admin) / 100, 4)).replace(".", ",")
        return admin_form

    def write_content(self, amount, term):
        """Writes the content into the CSV file"""
        with open('./sb_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
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
        chrome.get("https://www.sblizingas.lt/vartojimo-kreditas/kredito-gavimas/")
        self.cookie_monster()
        self.get_calculator()
        for term in self.terms:
            self.set_term(term)
            temp = self.temporary()
            for amount in self.amounts:
                if (amount == 100 and term > 12) or (amount == 500 and term > 30):
                    pass
                    # 100€ and smaller amounts are not issued for terms longer than 12 months, so these combos are escaped
                    # Same goes for 500€ and terms exceeding 30 months
                else:
                    if amount == 20 and temp != "--":
                        self.set_amount(amount)
                        self.waiter_small()
                        with open('./sb_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
                            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            csv_writer.writerow(["--", "--", "--"])
                        temp = self.temporary()
                    else:
                        self.set_amount(amount)
                        self.waiter(temp)
                        self.write_content(amount, term)
                        temp = self.temporary()
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through SB's data is {total_time} minutes.")
