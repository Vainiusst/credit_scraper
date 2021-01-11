import time
from datetime import timedelta
import sys
import csv
from c24 import C24
from bigbank import Bigbank
from bobute import Bobute
from gf import GF
from inbank import Inbank
from moki import Moki
from moment import Moment
from sb import SB
from smspinigai import Smspinigai
from fjord import Fjord
from tfbank import Tfbank

class Scraper:

    def __init__(self):
        self.directory = {
            '1': {
                "name": "c24",
                "columns": 4,
                "module": C24
            },
            '2': {
                "name": 'bigbank',
                "columns": 2,
                "module": Bigbank
            },
            '3': {
                "name": "bobute",
                "columns": 5,
                "module": Bobute
            },
            '4': {
                "name": "gf",
                "columns": 5,
                "module": GF
            },
            '5': {
                "name": "inbank",
                "columns": 4,
                "module": Inbank
            },
            '6': {
                "name": "moki",
                "columns": 5,
                "module": Moki
            },
            '7': {
                "name": "moment",
                "columns": 5,
                "module": Moment
            },
            '8': {
                "name": "sb",
                "columns": 5,
                "module": SB
            },
            '9': {
                "name": "smspinigai",
                "columns": 5,
                "module": Smspinigai
            },
            '10': {
                "name": "fjord",
                "columns": 2,
                "module": Fjord
            },
            '11': {
                "name": "tfbank",
                "columns": 2,
                "module": Tfbank
            }
        }

    def csv_checker(self, name):
        """Checks the number of rows in a CSV file.
        This is necessary to determine whether the CSV file is full or not."""
        with open(f"{name}_content.csv", mode='r') as file:
            return len(list(csv.reader(file)))

    def eraser(self, dic, input):
        """Erases and formats a particular CSV file"""
        name = dic[input]["name"]
        with open(f"./{name}_content.csv", newline='', mode='w', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if dic[input]["columns"] == 2:
                writer.writerow(["combination","installment", "contract"])
            elif dic[input]["columns"] == 4:
                writer.writerow(["combination", "installment", "interest", "APR", "contract"])
            elif dic[input]["columns"] == 5:
                writer.writerow(["combination", "installment", "interest", "APR", "admin", "contract"])

    def super_eraser(self, dic):
        """Erases and formats all of the CSV files"""
        for item in dic:
            self.eraser(dic, item)

    def after_scraping(self):
        response = input("Would You like to do anything else? Press Y if You'd like to scrape some more: ")
        if response == "Y" or response == 'y':
            self.scraper()
        else:
            sys.exit()

    def scraper(self):
        """Performs the scraping. This is the main method of the program."""
        print ("What would You like to scrape?\n1. Credit24\n2. BigBank\n3. Bobutės Paskola\n4. General Financing\n"
                "5. InBank\n6. Mokilizingas\n7. Moment Credit\n8. SB lizingas\n9. Smspinigai\n10. Fjordbank\n11. TF bank"
                "\n12. All\n13. Format CSV files\n14. Exit")
        inp = input("Enter your choice's number: ")
        inp_int = int(inp)
        start = time.time()
        if inp_int in range(1, 12):
            self.eraser(self.directory, inp)
            self.directory[inp]["module"]().main()
        elif inp_int == 12:
            for item in self.directory:
                if self.csv_checker(self.directory[item]["name"]) == 1:
                    self.directory[item]["module"]().main()
                else:
                    print(f"{self.directory[item]['name']} has been skipped because the corresponding CSV was not empty.")
        elif inp_int == 13:
            self.super_eraser(self.directory)
        elif inp_int == 14:
            sys.exit()
        end = time.time()
        time_spent = timedelta(seconds=end-start)
        print(f"Wew! That was quite a work! All in all, it took me some {time_spent} minutes to finish with this!")
        self.after_scraping()

#Code happens here:

print("Howdy pal! Let's do some scraping!")

Scraper().scraper()
