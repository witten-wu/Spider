from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re, time, requests, sys

print("Starting Chrome 远程调试......")
time.sleep(2)
# user_data_dir = r"C:\Users\Lab workstation\Desktop\chromedriver-win64"
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\Lab workstation\Desktop\chromedriver-win64"

try:
    url = "http://127.0.0.1:9222/json/version"
    response = requests.get(url)

    if response.status_code != 200:
        print("Chrome 远程调试 started failed")
        sys.exit(1)
except:
    print("Chrome 远程调试 started failed")
    sys.exit(1)


try:
    print("Connecting to Chrome......")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = Chrome(options=chrome_options)
except:
    print("Chrome connected failed")
    sys.exit(1)

time.sleep(2)
print("Connecting to 网易外贸通......")
driver.get('https://waimao.office.163.com/')
time.sleep(5)
print("请检查 Chrome 界面是否成功登录外贸通, 如未登录请于计时30s内手动进行登录, 登录成功后无需操作等待程序自动运行......")

wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/div[1]/div[2]/a[4]")))
customer_dev_link = driver.find_element(By.XPATH, "//*[@id='gatsby-focus-wrapper']/div/div[1]/section/div[1]/div[2]/a[4]")
customer_dev_url = customer_dev_link.get_attribute("href")
print("Login success, 正在跳转至数据抓取页面......")
driver.get(customer_dev_url)
time.sleep(10)
print("请于页面内手动设置筛选条件确定数据抓取范围, 计时1分钟后将自动对数据进行抓取......")
time.sleep(60)

def extract_email_addresses(table_element):
    email_addresses = []
    cells = table_element.find_elements(By.CSS_SELECTOR, "td.__address_antd_dropdown.ant-table-cell.index-module--min-width-cell--OPnGf.index-module--max-width-cell--Hl7kz.index-module--one-index--7ihdS.__address_antd_dropdown.ant-table-cell-fix-left.__address_antd_dropdown.ant-table-cell-fix-left-last.__address_antd_dropdown.ant-table-cell-ellipsis")
    max_retries = 3
    for cell in cells:
        cell_text = "N/A"
        for _ in range(max_retries):
            try:
                cell_text = cell.text
                break
            except:
                time.sleep(1)
        if cell_text == "N/A":
            continue
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, cell_text)
        if email_match:
            email_address = email_match.group()
            email_addresses.append(email_address)
    return email_addresses

print("===>准备抓取数据, please wait......")
time.sleep(5)
print("===>请注意: 程序运行期间请勿关闭 Chrome, 并请始终保持 Chrome 窗口在前台显示 (不要最小化), 且请手动关闭外贸通网页上出现的任何弹窗界面, 防止弹窗阻塞程序运行......")
time.sleep(10)
print("===>Start Now......")
while True:
    address_table_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.__address_antd_dropdown.ant-table-content")))
    table_element = address_table_div.find_element(By.TAG_NAME, "table")
    time.sleep(2)
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

print("===>End......")
print("===>数据抓取完毕! 数据文件保存为同级目录下的email_addresses.txt")
input("Press Enter to exit...")