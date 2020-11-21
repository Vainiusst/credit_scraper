import time
from datetime import timedelta
import sys
import csv_eraser
import csv
from c24 import C24

#Functions defined here:

def csv_checker(input):
    names = {
        '1': 'c24',
        '2': 'bgbank',
        '3': 'bobute',
        '4': 'gf',
        '5': 'inbank',
        '6': 'moki',
        '7': 'moment',
        '8': 'sb',
        '9': 'smspinigai',
        '10': 'fjord',
        '11': 'tfbank'
    }
    with open(f'{names[input]}_content.csv', mode='r') as file:
        return len(list(csv.reader(file)))


def scraper():
    print ("What would You like to scrape?\n1. Credit24\n2. BigBank\n3. Bobutės Paskola\n4. General Financing\n"
            "5. InBank\n6. Mokilizingas\n7. Moment Credit\n8. SB lizingas\n9. Smspinigai\n10. Fjordbank\n11. TF bank"
            "\n12. All\n13. Format CSV files\n14. Exit")
    inp = input("Enter your choice's number: ")
    inp_int = int(inp)
    start = time.time()
    if inp_int == 1:
        csv_checker(inp)
        C24().main()
    elif inp_int == 2:
        import bigbank
    elif inp_int == 3:
        import bobute
    elif inp_int == 4:
        import gf
    elif inp_int == 5:
        import inbank
    elif inp_int == 6:
        import moki
    elif inp_int == 7:
        import moment
    elif inp_int == 8:
        import sb
    elif inp_int == 9:
        import smspinigai
    elif inp_int == 10:
        import fjord
    elif inp_int == 11:
        import tfbank
    elif inp_int == 12:
        import bigbank
        import c24
        import fjord
        import gf
        import inbank
        import moki
        import moment
        import sb
        import smspinigai
        import bobute
        import tfbank
    elif inp_int == 13:
        csv_eraser.super_eraser()
    elif inp_int == 14:
        sys.exit()
    end = time.time()
    time_spent = timedelta(seconds=end-start)
    print(f"Wew! That was quite a work! All in all, it took me some {time_spent} minutes to finish with this!")
    inpt = input("Would You like to do anything else? Press Y if You'd like to scrape some more: ")
    if inpt == "Y" or inpt == 'y':
        scraper()
    else:
        sys.exit()


#Code happens here:

print("Howdy pal! Let's do some scraping!")

scraper()
