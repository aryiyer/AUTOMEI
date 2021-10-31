from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import datetime
import time

driver = webdriver.Chrome(executable_path='/Users/aryamaniyer/Desktop/chromedriver')
driver.get('https://scsi.sec.samsung.net/splus/mobilewebsapl/')

#finding login
userName = driver.find_element_by_id("UserId")
passWord = driver.find_element_by_id("Password")

#logging in
userName.send_keys("********")
passWord.send_keys("********")
passWord.send_keys(Keys.RETURN)

time.sleep(2)

#Getting date
x = datetime.datetime.now()
yyyy = str(x.year)
month = x.strftime("%B")
d = str(x.day - 4)
dateInput = str(d+"-"+month+"-"+yyyy)

#reading to list from csv
with open('sample.csv') as file:
   imeiReader = csv.reader(file)
   dataRaw = list(imeiReader)

def listToStr(li):
    return ("".join(li[0]))
#loop
count = 0
while count < len(dataRaw):
    #wait for shop to load
    try:
        shopCheck = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'shop'))
        )
    except:
        driver.quit()

    if count%5 == 0:
        selectShop = Select(driver.find_element_by_id('shop'))
        time.sleep(1)
        selectShop.select_by_value('1')
        selectDate = driver.find_element_by_id('scanDate')
        selectDate.send_keys(dateInput)

    imeiInput = driver.find_element_by_id('imei')
    imeiInput.send_keys(listToStr(dataRaw[count]))
    addButton = driver.find_element(By.XPATH, '//button[text()="Add"]')
    addButton.click()
    count += 1

    if count%5 == 0:
        submitButton = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        submitButton.click()
        time.sleep(8)
        driver.get('https://scsi.sec.samsung.net/splus/mobilewebsapl/#/imeiScan')
    elif count == len(dataRaw):
        submitButton = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        submitButton.click()
        time.sleep(8)
        driver.get('https://scsi.sec.samsung.net/splus/mobilewebsapl/#/imeiScan')


time.sleep(5)
print("success")
driver.quit()
