# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from time import sleep
#
# chrome = webdriver.Chrome()
# chrome.get("https://www.smspinigai.lt")
#
# slider = chrome.find_element_by_xpath('//*[@id="slider_summa"]/div[2]/div[2]/div')
# move = ActionChains(chrome)
# move.click_and_hold(slider).move_by_offset(-204, 0).release().perform()
# sleep(0.5)
#
# '''
# Atstumas - 537, 26 aktyvūs taškai. Tarp taškų, teoriškai - 20,6538. Nuo 100 iki 200 - 14. Nuo 100 iki 300 - 41.
# Nuo 100 iki 400 - 68. Nuo 100 iki 500 - 96. Nuo 100 iki 600 - 120
# Tarpai tarp pagrindinių 5 skirnsnių yra apytiksliai 107 pts.
# 1, 3, 4 skirsniai, suma padidėja maždaug kas 26-27 pts
# 2 skirsnyje - kas maždaug 21
# 5 skirsnyje, kas 13,5
# '''
#
# move.click_and_hold(slider).move_by_offset(107, 0).release().perform()
# sleep(1)

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

chrome = webdriver.Chrome()
chrome.get("https://www.smspinigai.lt")

slider = chrome.find_element_by_xpath('//*[@id="slider_period"]/div[2]/div[2]/div/div[1]')
move = ActionChains(chrome)
move.click_and_hold(slider).move_by_offset(1, 0).release().perform()
sleep(1)
move.click_and_hold(slider).move_by_offset(0.5, 0).release().perform()
sleep(1)
