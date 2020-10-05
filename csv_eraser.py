import csv

def bigbank_eraser():
    with open("./bigbank_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment"])

def bobute_eraser():
    with open("./bobute_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def credit24_eraser():
    with open("./credit24_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR"])

def gf_eraser():
    with open("./gf_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def inbank_eraser():
    with open("./inbank_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR"])

def moki_eraser():
    with open("./moki_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def moment_eraser():
    with open("./moment_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def sb_eraser():
    with open("./sb_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def smspinigai_eraser():
    with open("./smspinigai_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def fjord_eraser():
    with open("./fjordbank_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination", "installment"])

def vivus_eraser():
    with open("./vivus_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

def tfbank_eraser():
    with open("./tfbank_content.csv", newline='', mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["combination","installment","interest","APR","admin"])

bigbank_eraser()
bobute_eraser()
credit24_eraser()
gf_eraser()
inbank_eraser()
moki_eraser()
moment_eraser()
sb_eraser()
smspinigai_eraser()
fjord_eraser()
vivus_eraser()
