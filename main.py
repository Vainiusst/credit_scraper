import time
from datetime import timedelta
import sys

#Functions defined here:
def scraper():
    print ("What would You like to scrape?\n1. Credit24\n2. BigBank\n3. Bobutės Paskola\n4. General Financing\n"
            "5. InBank\n6. Mokilizingas\n7. Moment Credit\n8. SB lizingas\n9. Smspinigai\n10. Fjordbank\n 11. TF bank"
            "\n12. Vivus.lt\n13. All\n14. Format CSV files\n15. Exit")
    inp = int(input("Enter your choice's number: "))
    start = time.time()
    if inp == 1:
        import c24
    elif inp == 2:
        import bigbank
    elif inp == 3:
        import bobute
    elif inp == 4:
        import gf
    elif inp == 5:
        import inbank
    elif inp == 6:
        import moki
    elif inp == 7:
        import moment
    elif inp == 8:
        import sb
    elif inp == 9:
        import smspinigai
    elif inp == 10:
        import fjord
    elif inp == 11:
        import tfbank
    elif inp == 12:
        import vivus
    elif inp == 13:
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
        import vivus
        import tfbank
    elif inp == 14:
        import csv_eraser
    elif inp == 15:
        sys.exit()
    end = time.time()
    time_spent = timedelta(seconds=end-start)
    print(f"Wew! That was quite a work! All in all, it took me some {time_spent} minutes to finish with this!")
    inpt = input("Would You like to do anything else? Press Y if You'd like to scrape some more: ")
    if inpt == "Y" or inpt == 'y':
        scraper()
    else:
        return


#Code happens here:

print("Howdy pal! Let's do some scraping!")

scraper()
