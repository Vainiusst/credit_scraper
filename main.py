from time import time
from datetime import timedelta
import sys

#Functions defined here:
def scraper():
    print ("What would You lke to scrape?\n1. Credit24\n2. BigBank\n3. Bobutės Paskola\n4. General Financing\n"
           "5. InBank\n6. Mokilizingas\n7. Moment Credit\n8. SB lizingas\n9. Smspinigai\n10. All\n11. Exit")
    inp = int(input("Enter your choice's number: "))
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
        import c24
        import bigbank
        import bobute
        import gf
        import inbank
        import moki
        import moment
        import sb
        import smspinigai
    elif inp == 11:
        sys.exit()
    end = time.time()
    time_spent = timedelta(seconds=end - start)


#Code happens here:
start = time.time()

print("Howdy pal! Let's do some scraping!")
scraper()
print(f"Wew! That was quite a work! All in all, it took me some {time_spent} minutes to finish with this!")

inpt = ("Is this all? Y/N: ")
if inpt == "Y":
    sys.exit(0)
else:
    scraper()
