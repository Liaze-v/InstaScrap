from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time, random
import csv


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



# Instagram username list for DM:
# On recup les noms des utilisateures scraper 
usernames =[] # Tableau qui contient les noms des utilisateures
subusernames=[] # Tableau qui contient les sous noms des uitilisateures
with open('scrap.csv', encoding="utf-8", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        # print(row[1])
        usernames.append(row[1])
        try:
            subusernames.append(row[2])
        except IndexError:
            subusernames.append(None)
            continue


# Messages:
messages = ['Hey! Pls follow my page', 'Hey, how you doing?', 'Hey']

# Delay time between messages in sec:
between_messages = 300

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
    
    
    
    
    
    
def send_message(users, messages):
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a').click()
    
    time.sleep(random.randrange(3,5))
    # driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
    # time.sleep(random.randrange(1,2))
    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
    time.sleep(random.randrange(1,2))
    for user in users:
        time.sleep(random.randrange(1,2))
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/div/div[2]/input').send_keys(user)
        time.sleep(random.randrange(2,3))
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]').find_element(By.TAG_NAME,'button').click()
        time.sleep(random.randrange(3,4))
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div/button').click()
        time.sleep(random.randrange(3,4))
        text_area = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        text_area.send_keys(random.choice(messages))
        time.sleep(random.randrange(2,4))
        # text_area.send_keys(Keys.ENTER)
        print(f'Message successfully sent to {user}')
        time.sleep(between_messages)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()

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

# envoie des messages
send_message(usernames, messages)

