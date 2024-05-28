from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re, time

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = Chrome(options=chrome_options)

driver.get('https://waimao.office.163.com/')

wait = WebDriverWait(driver, 20)

# click 客户发现
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/div[1]/div[2]/a[4]")))
customer_dev_link = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/div[1]/div[2]/a[4]")
customer_dev_url = customer_dev_link.get_attribute("href")
driver.get(customer_dev_url)
print(customer_dev_url)
# click 分组
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div[2]")))
customer_dev_link = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div[2]") 
customer_dev_link.click() 
print(driver.current_url)
# click Joyce
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[2]/td[1]/div/span[1]/span[1]")))
customer_dev_link = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[2]/td[1]/div/span[1]/span[1]") 
customer_dev_link.click() 
print(driver.current_url)

# extract email address
def extract_email_addresses(table_element):
    email_addresses = []
    rows = table_element.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        for cell in cells:
            cell_text = cell.text
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_match = re.search(email_pattern, cell_text)
            if email_match:
                email_address = email_match.group()
                email_addresses.append(email_address)
    return email_addresses

while True:
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/table")))
    table_element = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/table")
    time.sleep(5)

    email_addresses = extract_email_addresses(table_element)
    
    with open("email_addresses.txt", "a") as f:
        for email_address in email_addresses:
            f.write(email_address + "\n")
            print(email_address)
    
    nextpage = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next")
    next_page_button = nextpage.find_element(By.CSS_SELECTOR, "button")
    if nextpage.get_attribute("aria-disabled") == "false": 
        next_page_button.click()
    else:
        break

# wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/table")))
# email_element = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/table")
# time.sleep(10)
# rows = email_element.find_elements(By.TAG_NAME, "tr")
# email_addresses = []
# for row in rows:
#     cells = row.find_elements(By.TAG_NAME, "td")
#     for cell in cells:
#         cell_text = cell.text
#         email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         email_match = re.search(email_pattern, cell_text)
#         if email_match:
#             email_address = email_match.group()
#             email_addresses.append(email_address)
# for email_address in email_addresses:
#     print(email_address)
# wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/ul/li[10]/button")))
# nextpage = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/ul/li[10]/button")
# nextpage.click() 
# time.sleep(10)
# wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/table")))
# email_element = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/section/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/table")
# rows = email_element.find_elements(By.TAG_NAME, "tr")
# email_addresses = []
# for row in rows:
#     cells = row.find_elements(By.TAG_NAME, "td")
#     for cell in cells:
#         cell_text = cell.text
#         email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         email_match = re.search(email_pattern, cell_text)
#         if email_match:
#             email_address = email_match.group()
#             email_addresses.append(email_address)
# for email_address in email_addresses:
#     print(email_address)


# from selenium import webdriver 
# from time import sleep
# browser = webdriver.Chrome()  
# browser.maximize_window()
# browser.get('https://www.google.com/')  
# sleep(100)


# from selenium import webdriver
# import os
# import time
# import json
 
# def browser_initial():
#     """"
#     进行浏览器初始化
#     """
#     os.chdir(r'C:\Users\Lab workstation\Desktop\chromedriver-win64')
#     browser = webdriver.Chrome()
#     log_url = 'https://waimao.office.163.com/login/'
#     return log_url,browser
 
# def get_cookies(log_url,browser):
#     """
#     获取cookies保存至本地
#     """
#     browser.get(log_url)
#     time.sleep(30)     # 进行扫码
#     dictCookies = browser.get_cookies()
#     jsonCookies = json.dumps(dictCookies) #  转换成字符串保存
#     with open('cookies.txt', 'w') as f:
#         f.write(jsonCookies)
#     print('cookies保存成功！')
 
# if __name__ == "__main__":
#     tur = browser_initial()
#     get_cookies(tur[0], tur[1])

# from selenium import webdriver
# import os
# import time
# import json


# def browser_initial():
#     os.chdir(r'C:\Users\Lab workstation\Desktop\chromedriver-win64')
#     browser = webdriver.Chrome()
#     goal_url = 'https://waimao.office.163.com/#intelliMarketing?page=addressContactList&keyName=addressContactList-1716865562218'
#     browser.get(goal_url)
#     return goal_url, browser
 
# def log_waimao(goal_url, browser):
#     with open('cookies.txt', 'r', encoding='utf8') as f:
#         listCookies = json.loads(f.read())
#     # 往browser里添加cookies
#     for cookie in listCookies:
#         cookie_dict = {
#             'domain': cookie.get('domain'),
#             'name': cookie.get('name'),
#             'value': cookie.get('value'),
#             'path': '/',
#             "sameSite": 'None',
#             'secure': False,
#             'httpOnly': False
#         }
#         browser.add_cookie(cookie_dict)
#     browser.get(goal_url)                 
#     time.sleep(100) 
    
# if __name__ == "__main__":
#     tur = browser_initial()
#     log_waimao(tur[0],tur[1])


# from selenium import webdriver
# import os
# import time
# import json
# # 登录
# def login_jd():
#     browser = webdriver.Chrome()
#     # 登录前清除所有cookie
#     browser.get('https://waimao.office.163.com/login/')
#     browser.delete_all_cookies()
#     list_cookies = [{'domain': '.office.163.com', 'httpOnly': False, 'name': 'Coremail', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1#V*seXP7mck*7y61*AntpqhQ*rBeynv4PGoDKaP7a0azKyiNOS8Flig2mMaDOVVil7Rf-b*SFNEgnPcG5V7wyxohxawmm*JjHaW9wkl31pRJU2wTQtIaPTwHaHAa5zyYwv5McuvOQf8G4K-0I9uTfGXp2XVPikDdqssjQt16QmGQ|%js6-21-1'}, {'domain': '.office.163.com', 'httpOnly': False, 'name': 'QIYE_TOKEN', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0MTZiNmY0Mi04M2YzLTQ3OGItYTgzZS03ODYwMGU0ZTU4NTUiLCJzdWIiOiJBdXRoIiwidXNlckluZm8iOnsiYXBwSWQiOiJzaXJpdXMiLCJ1c2VySWQiOiI1NDg0ODk0MjIiLCJpcCI6IjEzNy4xODkuMTU4LjkiLCJleHBpcmVzIjo2MDQ4MDB9LCJleHAiOjE3MTc0NzQxMDF9.v4excEUqsVOZm8cZLXiBzvBidYhKn9J0PDXVgzdlsL8'}, {'domain': '.office.163.com', 'expiry': 1719490099, 'httpOnly': True, 'name': '_deviceId', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '4b2a16a0a3b4cdb8782815236af96a7c'}, {'domain': '.office.163.com', 'httpOnly': False, 'name': 'bh', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'queenie@uudeee.com'}, {'domain': '.office.163.com', 'httpOnly': False, 'name': 'mail_idc', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'mg.127.net'}, {'domain': '.office.163.com', 'httpOnly': False, 'name': 'qiye_uid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '"queenie@uudeee.com"'}, {'domain': '.office.163.com', 'httpOnly': False, 'name': 'QIYE_SESS', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'k4hMEf9KyjwiI3z_p51Is8L8ODH9bRrg9W3ajZoCzNtOusgwBUJpKS7CFuCdOTr_biXdAbs8lFFxhyn4HUUzSUfKBUzmIbBn8rxmT_YvxzMkwKdiMJLPC3R1OaUYJtzmyIXQkK3QrVBnZBhaleQyA_i1bvHzX3YK2VHZlKzihzG'}]
#     #   time.sleep(20)  
#     # 获取之后的cookie
#     #   cookies = browser.get_cookies()
#     #   print(browser.get_cookies())
#     # 将获取的的所有cookies添加到浏览器
#     for cookie in list_cookies:
#         browser.add_cookie(cookie)
#     browser.get('https://waimao.office.163.com/#intelliMarketing?page=addressContactList&keyName=addressContactList-1716865562218')                 
#     time.sleep(100) 

# if __name__ == "__main__":
#     login_jd()

