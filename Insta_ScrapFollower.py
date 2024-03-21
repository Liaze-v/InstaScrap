from tkinter import Variable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time, random
from bs4 import BeautifulSoup
import csv
from datetime import datetime  
# import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



option = webdriver.ChromeOptions()
#set chrome to french, so we can find element easiler 
option.add_argument('--lang=fr')
#change size of chrome (option)
option.add_argument('--window-size=1200,1000')



# Username and password of your instagram account:
my_username = ''
my_password = ''

# Username and password of your instagram account:INPUT
# my_username=input('Enter Your Username:')
# my_password=input('Enter Password:')

# url pour scrap:
url = ""

# url pour scrap:
# url = input('Enter Url:')


# Vas chercher chromedriver
service = Service(executable_path="chromedriver.exe")
# lance chromedriver
driver = webdriver.Chrome(service=service)



def auth(username, password):
    # Vas sur le site instagram
    driver.get('https://instagram.com')
    time.sleep(random.randrange(2,4))
    # Accepte les cookies
    driver.find_element(By.XPATH,'/html/body/div[4]/div/div/button[2]').click()
    # On chercher les elements champ user et pass
    input_username = driver.find_element(By.NAME,'username')
    input_password = driver.find_element(By.NAME,'password')
    
    # On entre le user et pass dans les champ
    input_username.send_keys(username)
    time.sleep(random.randrange(1,2))
    input_password.send_keys(password)
    time.sleep(random.randrange(1,2))
    input_password.send_keys(Keys.ENTER)
    


def scrap():
    scrapArray= [['Link','Name','SubName']]
    elements = driver.find_elements(By.XPATH,"//div[@class='x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe']/div/div/div[2]/div/div/div/div[2]") 
    for WebElement in range(len(elements)):
        arrayPersornne= []
        # Scrap Lien
        elementHTML = elements[WebElement].get_attribute('outerHTML') #gives exact HTML content of the element
        elementSoup = BeautifulSoup(elementHTML,'html.parser')
        soup = BeautifulSoup(elementHTML, 'html.parser')
        links = soup.find_all("a")
        for link in links:
            # print("https://www.instagram.com"+str(link.get("href")))
            arrayPersornne.append("https://www.instagram.com"+str(link.get("href")))
        # Scrap nom 
        namedivs = elements[WebElement].find_elements(By.XPATH,"./div[1]")
        for namediv in namedivs:
            soup2 = BeautifulSoup(namediv.text, 'html.parser')
            arrayPersornne.append(str(soup2))
        subnamedivs = elements[WebElement].find_elements(By.XPATH,"./div[2]")
        for subnamediv in subnamedivs:
            soup3 = BeautifulSoup(subnamediv.text, 'html.parser')
            arrayPersornne.append(str(soup3))
        scrapArray.append(arrayPersornne)
        save(scrapArray)


# TEXTE 
# open file in write mode
def save(scrapArray):
    try:
        f = open('scrap.csv', 'a', encoding="utf-8", newline='')  #utf-8
        df = pd.read_csv('scrap.csv', sep=",")
        for item in scrapArray:
            if item[0] in df['Link'].values:
                continue
            else:
                with f:
                    writer = csv.writer(f)
                    writer.writerows([item])
    except:
        print('eror')
        f = open('scrap.csv', 'w', encoding="utf-8", newline='')  #utf-8
        print('Fichier pandas non ouvert') 
        with f:
            writer = csv.writer(f)
            writer.writerows(scrapArray)





# autenthification
auth(my_username, my_password)
time.sleep(random.randrange(15,30))


# Notification
# wait fro login success
time.sleep(random.randrange(1,2))       
driver.find_element(By.XPATH,"//button[contains(text(),'Plus tard')]").click()
time.sleep(random.randrange(3,6))  
driver.find_element(By.XPATH,"//button[contains(text(),'Plus tard')]").click()
time.sleep(random.randrange(1,2))
# On go sur l'url pour scrap
driver.get(url)
time.sleep(random.randrange(2,4))
#click on following button(People you are following; people you like)
driver.find_element(By.XPATH,"//a[contains(@href, '/followers')]").click()
time.sleep(random.randrange(2,4))


# copy the xpath of scrollbar
scroll_box = driver.find_element(By.XPATH,"//div[@class='x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe']")
time.sleep(random.randrange(2,4))
# height variable
last_ht, ht = 0, 1
while last_ht != ht:
    last_ht = ht
    time.sleep(random.randrange(5,8))
    result = None
    while result is None:
        try:
            result = driver.find_element(By.CLASS_NAME, '_aanq')
        except:
            time.sleep(random.randrange(2,4))
            pass
    # wait = WebDriverWait(driver, 20)
    # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_aanq')))
    try:
        driver.execute_script('document.querySelector("._aano").scrollTo(0, document.querySelector("._aano").scrollHeight);')
        ht = driver.execute_script('return document.querySelector("._aano").scrollHeight;')
    except:
        pass
    scrap()
    # Prevent error of scrap due to scroll of instagram. Ask user if he wants to continue
    print(last_ht, ht)
    if (last_ht == ht):
        oncontinue = input('Est ce que le Scraping est fini ?  y/n')
        if(oncontinue == 'n'):
            break
        else:
            last_ht = ht - 10


time.sleep(random.randrange(2,4))
links = scroll_box.find_element(By.TAG_NAME,'a')
time.sleep(random.randrange(2,4))


