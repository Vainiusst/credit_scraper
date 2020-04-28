import bigbank
import bobute
import c24
import gf
import inbank
import moki
import moment
import sb
import smspinigai
import time

start = time.time()

print("Howdy pal! Let's do some scraping!")
bigbank.do_erryfin(bigbank.amounts, bigbank.terms)
bobute.do_erryfin(bobute.amounts, bobute.terms)
gf.do_erryfin(gf.amounts, gf.terms)
inbank.do_erryfin(inbank.amounts, inbank.terms)
moki.do_erryfin(moki.amounts, moki.terms)
moment.do_erryfin(moment.amounts, moment.terms)
sb.do_erryfin(sb.amounts, sb.terms)
smspinigai.do_erryfin(smspinigai.amounts, smspinigai.terms)
try:
    c24.do_erryfin(c24.amounts)
except:
    print("Gosh darn! Credit24 ain't workin' properly!")
finally:
    end = time.time()
    time_spent = (end - start)/60
    print(f"Wew! That was quite a work! All in all, it took me some {time_spent} minutes to finish with this!")
