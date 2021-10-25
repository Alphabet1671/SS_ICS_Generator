import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



url = "https://portals.veracross.com/ssa/student/student/daily-schedule"

webUsnm = "23yel"
webPswd = "LiYe9716"
totDays = int(input("How many days of your schedule would you like to pull from Veracross?"))
driver = webdriver.Safari()
driver.get(url)
time.sleep(2)

usnmInput = driver.find_element(By.NAME, "username")
usnmInput.send_keys(webUsnm)
pswdInput = driver.find_element(By.NAME, "password")
pswdInput.send_keys(webPswd)


lginBtn = driver.find_element(By.NAME, "commit")
lginBtn.click()

"""eng of logins"""
table = open("blockSchedule.txt", "w", encoding = "UTF-8")
currentTime = datetime.datetime.now()
oneDay = datetime.timedelta(days=1)

count = 0
while(count<totDays):
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    if soup.find(class_="vx-heading-6 rotation-day-header"):
        dateText = soup.find(class_="vx-heading-4").get_text().replace(" ", "").replace("\n", "")
        cycleDay = soup.find(class_="vx-heading-6 rotation-day-header").get_text().replace(" ", "").replace("\n", "").replace("SSDay","")
        table.write(dateText+"+"+cycleDay+"\n")
        print(dateText+" is "+cycleDay)
    time.sleep(1)
    Btn = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div/a[3]")
    Btn.click()
    time.sleep(1)
    currentTime += oneDay
    count += 1


