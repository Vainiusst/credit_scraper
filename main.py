import time
from datetime import timedelta
import sys
import csv
from c24 import C24
from bigbank import Bigbank
from bobute import Bobute


directory = {
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
        "columns": 5
    },
    '5': {
        "name": "inbank",
        "columns": 4
    },
    '6': {
        "name": "moki",
        "columns": 5
    },
    '7': {
        "name": "moment",
        "columns": 5
    },
    '8': {
        "name": "sb",
        "columns": 5
    },
    '9': {
        "name": "smspinigai",
        "columns": 5
    },
    '10': {
        "name": "fjord",
        "columns": 2
    },
    '11': {
        "name": "tfbank",
        "columns": 2
    }
}

# def csv_checker(dict):
#     with open(f"{dict}_content.csv", mode='r') as file:
#         return len(list(csv.reader(file)))

def eraser(dict, input):
    with open(f"./{dict[input]['name']}_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if dict[input]["columns"] == 2:
            writer.writerow(["combination","installment"])
        elif dict[input]["columns"] == 4:
            writer.writerow(["combination", "installment", "interest", "APR"])
        elif dict[input]["columns"] == 5:
            writer.writerow(["combination", "installment", "interest", "APR", "admin"])

def super_eraser(dict):
    for item in dict:
        eraser(dict[item]["name"], dict[item]["columns"])

def scraper():
    print ("What would You like to scrape?\n1. Credit24\n2. BigBank\n3. Bobutės Paskola\n4. General Financing\n"
            "5. InBank\n6. Mokilizingas\n7. Moment Credit\n8. SB lizingas\n9. Smspinigai\n10. Fjordbank\n11. TF bank"
            "\n12. All\n13. Format CSV files\n14. Exit")
    inp = input("Enter your choice's number: ")
    inp_int = int(inp)
    start = time.time()
    if inp_int in range(1, 12):
        eraser(directory, inp)
        directory[inp]["module"]().main()
    # elif inp_int == 2:
    #     import bigbank
    # elif inp_int == 3:
    #     import bobute
    # elif inp_int == 4:
    #     import gf
    # elif inp_int == 5:
    #     import inbank
    # elif inp_int == 6:
    #     import moki
    # elif inp_int == 7:
    #     import moment
    # elif inp_int == 8:
    #     import sb
    # elif inp_int == 9:
    #     import smspinigai
    # elif inp_int == 10:
    #     import fjord
    # elif inp_int == 11:
    #     import tfbank
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
        super_eraser(arguments)
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
