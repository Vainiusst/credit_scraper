from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from time import time
from datetime import timedelta
import csv
import re


class Smspinigai:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.amounts= [-1, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0667, 0.0667, 0.0667]
        self.terms = [-0.2857, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429, 0.1429]

    def waiter(self, temp):
        """Pauses actions until certain text appears in the targeted element"""
        path = '//*[@id="calc_monthly"]'
        wdw(self.chrome, 10).until_not(ec.text_to_be_present_in_element((by.XPATH, path), temp))

    def waiter_dets(self):
        """Waits until the credit details are available for reading"""
        wdw(self.chrome, 10).until(ec.visibility_of_element_located((by.XPATH, '//*[@id="graph_modal"]')))

    def nuolatinis(self):
        """Presses the radio button to choose the 'Nuolatinis' option"""
        path = '/html/body/div[1]/div[1]/main/section/div/div[2]/div/ul/li[2]'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def vartojimo(self):
        """Presses the button to choose the consumer loan"""
        path = '/html/body/div[1]/div[1]/main/section/ul/li[3]/a'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def set_amount(self, amount):
        """Sets the desired amount"""
        bar_width = self.chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]').size["width"]
        slider = self.chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div/div[1]')
        move_amt = ActionChains(self.chrome)
        offset = amount * bar_width
        move_amt.drag_and_drop_by_offset(slider, offset, 0).perform()

    def set_term(self, term):
        """Sets the desired term"""
        bar_width = self.chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[1]').size["width"]
        slider = self.chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[2]/div/div[1]')
        move_term = ActionChains(self.chrome)
        offset = term * bar_width
        move_term.drag_and_drop_by_offset(slider, offset, 0).perform()

    def open_dets(self):
        """Opens the credit details"""
        path = '/html/body/div[1]/div[1]/main/section/div/div[2]/div/div[2]/a'
        wdw(self.chrome, 5).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def cookie_monster(self):
        """Closes the cookies' pop-up"""
        path = '//*[@id="cookie-vue-app"]/div/div/div[2]'
        wdw(self.chrome, 10).until(ec.element_to_be_clickable((by.XPATH, path)))
        self.chrome.find_element_by_xpath(path).click()

    def read_installment(self):
        """Reads and formats the installment to be written into the CSV"""
        installment = self.chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[3]').get_attribute("innerHTML")[:-2]
        inst_str = re.search('\d+,\d+', installment).group()
        return inst_str

    def read_interest(self):
        """Reads and formats the interest rate to be written into the CSV"""
        interest = self.chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[5]').get_attribute("innerHTML")[:-2]
        int_str = re.search('\d+,\d+', interest).group().replace(",", ".")
        int_form = str(round(float(int_str)/100, 4)).replace(".", ",")
        return int_form

    def read_APR(self):
        """Reads and formats the APR to be written into the CSV"""
        APR = self.chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[6]').get_attribute("innerHTML")[:-2]
        APR_str = re.search('\d+,\d+', APR).group().replace(",", ".")
        APR_form = str(round(float(APR_str)/100, 4)).replace(".", ",")
        return APR_form

    def read_admin(self):
        """Reads and formats the admin fee to be written into the CSV"""
        admin = self.chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[4]').get_attribute("innerHTML")[:-2]
        admin_str = re.search('\d+,\d+', admin).group()
        return admin_str

    def turn_to_proc(self, func):
        """Since read_admin() only acquires admin fee in €, I need to change it to percentage.
        This function does that."""
        number = func.replace(",", ".")
        number_fl = float(number)
        amount = self.chrome.find_element_by_xpath('//*[@id="graph_modal"]/ul/li[1]').get_attribute("innerHTML")[:-2]
        amount_fl = float(re.search('\d+,\d+', amount).group().replace(",", "."))
        proc = str((number_fl)/amount_fl)
        proc_str = proc.replace(".", ",")
        return proc_str

    def to_mths(self, string):
        """Reads and formats the term as shown in the browser,
        because parameters sent to the functions are offsets, not actual months"""
        if string[2:] == " mėn.":
            return int(string[1])
        else:
            no_yrs = int(string[0])
            return no_yrs*12

    def write_content(self):
        """Writes contents into the CSV file"""
        with open('./smspinigai_content.csv', newline='', mode='a', encoding='UTF-8') as db2:
            suma = self.chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div/div[2]/span/span').get_attribute("innerHTML")[:-2]
            terminas_pre = self.chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[2]/div/div[2]/span/span').get_attribute("innerHTML")
            terminas = self.to_mths(terminas_pre)
            combo = f'{suma}/{terminas}'
            installment = self.read_installment()
            interest = self.read_interest()
            APR = self.read_APR()
            admin = self.turn_to_proc(self.read_admin())
            csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([combo, installment, interest, APR, admin])

    def close_dets(self):
        """Closes the credit details"""
        close_bttn = self.chrome.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/span')
        close_bttn.click()

    def do_erryfin(self, amounts, terms):
        """Combines all of the actions necessary for the program to run into a single function"""
        self.chrome.maximize_window()
        self.chrome.get("https://www.smspinigai.lt")
        self.cookie_monster()
        self.vartojimo()
        self.nuolatinis()
        counter = 0
        for term in self.terms:
            self.set_term(term)
            for amount in self.amounts:
                if counter == 0:
                    self.set_amount(amount)
                    self.open_dets()
                    self.waiter_dets()
                    self.write_content()
                    self.close_dets()
                    counter += 1
                else:
                    temp = self.chrome.find_element_by_xpath('//*[@id="calc_monthly"]').get_attribute("innerHTML")
                    self.set_amount(amount)
                    try:
                        self.waiter(temp)
                    except:
                        pass
                    self.open_dets()
                    self.waiter_dets()
                    self.write_content()
                    self.close_dets()
                    counter += 1
        self.chrome.close()

    def main(self):
        """Main method which scrapes the page for information and times the execution."""
        starting_time = time() # Starting time to check the duration of the program

        self.do_erryfin(self.amounts, self.terms)

        ending_time = time() # Ending time to check the duration of the program
        total_time = str(timedelta(seconds=ending_time - starting_time))
        print(f"Time to crunch through Smspinigai data is {total_time} minutes.")
