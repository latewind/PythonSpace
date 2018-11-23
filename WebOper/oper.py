from selenium import webdriver
import time


driver = webdriver.Firefox()

driver.get("https://passport.5173.com/?returnUrl=http%3A//www.5173.com/")
time.sleep(1)
driver.find_element_by_id("txtName").send_keys("13963409910")
time.sleep(1)
driver.find_element_by_id("txtPass").send_keys("wsmn2015")
time.sleep(1)
driver.find_element_by_id("asp").click()

time.sleep(3)

driver.get("http://trading.5173.com/auction/NewPublishV3.aspx?")

hover_close = driver.find_element_by_xpath("//li[contains(@class, 'hover_close')]")

if hover_close is not None:
    hover_close.click()













# webdriver.Chrome()