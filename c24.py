from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv


class C24():
    """Class for Credit24's page"""
    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts = [0, 0.0816327, 0.183673, 0.387755, 0.591837, 0.795918, 1]

    def waiter(self):
        """Waits until necessary elements are loaded and CSS animations stop"""
        path = '//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div[1]/div/div/div/div/span'
        wdw(self.chrome, 5).until(ec.text_to_be_present_in_element((by.XPATH, path), "1000 €"))

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        path = '//*[@id="onetrust-accept-btn-handler"]'
        wdw(self.chrome, 5).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def read_installment(self):
        """Reads the installment and returns it properly formatted to be written into the CSV file"""
        path = '//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[5]/div/span/div/div'
        installment = self.chrome.find_element_by_xpath(path)
        installment_iso = installment.get_attribute("innerHTML")[:-1]
        return installment_iso

    def read_interest(self):
        """Reads the interest and returns it properly formatted to be written into the CSV file"""
        path = '//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[8]/span/div/div'
        interest = self.chrome.find_element_by_xpath(path)
        interest_iso = interest.get_attribute("innerHTML")[:-1].replace(",", ".")
        interest_form = str(round(float(interest_iso)/100, 4)).replace(".", ",")
        return interest_form

    def read_APR(self):
        """Reads the APR and returns it properly formatted to be written into the CSV file"""
        path = '//*[@id="mainBanner"]/div[2]/div/div/div/div/div/div/div/div/div/div[9]/div/span/div/div'
        APR = self.chrome.find_element_by_xpath(path)
        APR_iso = APR.get_attribute("innerHTML")[:-1].replace(",", ".")
        APR_form = str(round(float(APR_iso) / 100, 4)).replace(".", ",")
        return APR_form

    def write_content(self):
        """Writes details into the CSV file"""
        with open('./c24_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            suma = self.chrome.find_element_by_xpath('//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[3]/div/div[1]/div/div/div/div/span')
            suma_iso = suma.get_attribute("innerHTML")[:-2]
            combo = f'{suma_iso}/36'
            installment = self.read_installment()
            interest = self.read_interest()
            APR = self.read_APR()
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment, interest, APR])

    def do_erryfin(self):
        """Combines all the necessary actions for the program to work into a single function"""
        chrome = self.chrome
        chrome.maximize_window()
        chrome.get("https://credit24.lt/")
        self.cookie_monster()
        self.waiter()
        move = ActionChains(chrome)
        slider_bar = chrome.find_element_by_xpath(
            '//*[@id="mainBanner"]/div/div/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/div[1]')
        sb_size = slider_bar.size
        sb_width = sb_size["width"]
        for amount in self.amounts:
            offset = sb_width*amount
            move.move_to_element_with_offset(slider_bar, offset, 0).click().perform()
            self.write_content()
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time()  # Starting time to check the duration of the program

        self.do_erryfin()

        ending_time = time()  # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Credit24's data is {total_time} minutes.")