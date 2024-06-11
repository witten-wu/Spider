import re, time, requests, sys
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


print("Starting Chrome Debug......")
time.sleep(1)
# user_data_dir = r"C:\Users\Lab workstation\Desktop\chromedriver-win64"
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\Lab workstation\Desktop\chromedriver-win64"

try:
    url = "http://127.0.0.1:9222/json/version"
    response = requests.get(url)

    if response.status_code != 200:
        print("Chrome Debug started failed")
        sys.exit(1)
except:
    print("Chrome Debug started failed")
    sys.exit(1)


try:
    print("Connecting to Chrome......")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = Chrome(options=chrome_options)
except:
    print("Chrome connected failed")
    sys.exit(1)

time.sleep(1)
print("Connecting to poe......")

driver.get('https://poe.com/')
time.sleep(3)
print("===> 1. Please check if you have successfully logged in to poe in Chrome, if not, please log in manually.")
print("===> 2. After successfully logged in, please switch to your prepared chat window.")
print("You will have 30s to complete the above two steps. Please wait for the program to run automatically after you done......")
time.sleep(3)

actions = ActionChains(driver)
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.GrowingTextArea_growWrap__im5W3.ChatMessageInputContainer_textArea__fNi6E")))
chatbox = driver.find_element(By.CSS_SELECTOR, "div.GrowingTextArea_growWrap__im5W3.ChatMessageInputContainer_textArea__fNi6E")
send_button = driver.find_element(By.CSS_SELECTOR, "button.Button_buttonBase__Bv9Vx.Button_primary__6UIn0.ChatMessageSendButton_sendButton__4ZyI4.ChatMessageInputContainer_sendButton__dBjTt")
print("===> Ready to start automated chat, please wait......")
print("Please don't close Chrome while the program is running, and always keep the Chrome window in the foreground (do not minimize it)")
time.sleep(3)

print("===> Pre-Processing Materials......")
df_prompt = pd.read_excel('Pretest GPT prompts.xlsx')
cropped_df_prompt = df_prompt.iloc[0:3, 2]
df_material = pd.read_excel('pretest material.xlsx')
# df_material = pd.read_excel('pretest material 0607 - Copy.xlsx')
cropped_df_material = df_material.iloc[0:, [3, 4, 5, 6, 9]]
print("===> Done")
print("===> Start Now......")


def get_poe_response(actions, driver, chatbox, send_button, question):
    time.sleep(3)
    answer = ""
    actions.send_keys_to_element(chatbox, question).perform()
    button_status = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_buttonBase__Bv9Vx.Button_primary__6UIn0.ChatMessageSendButton_sendButton__4ZyI4.ChatMessageInputContainer_sendButton__dBjTt")))
    if button_status:
        all_markdown_containers = driver.find_elements(By.CSS_SELECTOR, 'div.Markdown_markdownContainer__Tz3HQ')
        if all_markdown_containers:
            last_markdown_container = all_markdown_containers[-1]
            answer = last_markdown_container.text
        else:
            answer = "error:"
        send_button.click()
        return answer 
    else:
        answer = "error"
        return answer 

Q1_answer_list = []
Q1_score_list = []
Q1_2_answer_list = []
Q1_2_score_list = []
Q2_answer_list = []
Q2_score_list = []
Q2_2_answer_list = []
Q2_2_score_list = []
Q3_answer_list = []
Q3_score_list = []
for index, row in cropped_df_material.iterrows():
    Q1 = cropped_df_prompt.iloc[0]
    Q2 = cropped_df_prompt.iloc[1]
    Q3 = cropped_df_prompt.iloc[2]
    
    LITERAL_EXPLANATION = row.iloc[0]
    METAPHORICAL_EXPLANATION = row.iloc[1]
    TARGET = row.iloc[2]
    COMPETITOR = row.iloc[3]
    VEHICLE = row.iloc[4]
    
    new_Q1 = Q1.replace('EXPLANATION', LITERAL_EXPLANATION)
    new_Q1_2 = Q1.replace('EXPLANATION', METAPHORICAL_EXPLANATION)
    new_Q2 = Q2.replace('EXPLANATION', LITERAL_EXPLANATION)
    new_Q2_2 = Q2.replace('EXPLANATION', METAPHORICAL_EXPLANATION)
    new_Q3 = Q3.replace('TARGET', TARGET)
    new_Q3 = new_Q3.replace('EXPLANATION', METAPHORICAL_EXPLANATION)
    new_Q3 = new_Q3.replace('COMPETITOR', COMPETITOR)
    new_Q3 = new_Q3.replace('VEHICLE', VEHICLE)
    
    Q3_answer = get_poe_response(actions, driver, chatbox, send_button, new_Q1)
    Q1_answer = get_poe_response(actions, driver, chatbox, send_button, new_Q1_2)
    Q1_score = min([int(num) for num in re.findall(r'\d+', Q1_answer)])
    Q1_2_answer = get_poe_response(actions, driver, chatbox, send_button, new_Q2)
    Q1_2_score = min([int(num) for num in re.findall(r'\d+', Q1_2_answer)])
    Q2_answer = get_poe_response(actions, driver, chatbox, send_button, new_Q2_2)
    Q2_score = min([int(num) for num in re.findall(r'\d+', Q2_answer)])
    Q2_2_answer = get_poe_response(actions, driver, chatbox, send_button, new_Q3)
    Q2_2_score = min([int(num) for num in re.findall(r'\d+', Q2_2_answer)])
    
    if index != 0:
        Q3_answer_list.append(Q3_answer)
        Q3_score = min([int(num) for num in re.findall(r'\d+', Q3_answer)])
        Q3_score_list.append(Q3_score)
    Q1_answer_list.append(Q1_answer)
    Q1_score_list.append(Q1_score)
    Q1_2_answer_list.append(Q1_2_answer)
    Q1_2_score_list.append(Q1_2_score)
    Q2_answer_list.append(Q2_answer)
    Q2_score_list.append(Q2_score)
    Q2_2_answer_list.append(Q2_2_answer)
    Q2_2_score_list.append(Q2_2_score)
    

# collect the last answer
time.sleep(5)
actions.send_keys_to_element(chatbox, "END").perform()
button_status = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_buttonBase__Bv9Vx.Button_primary__6UIn0.ChatMessageSendButton_sendButton__4ZyI4.ChatMessageInputContainer_sendButton__dBjTt")))
if button_status:
    all_markdown_containers = driver.find_elements(By.CSS_SELECTOR, 'div.Markdown_markdownContainer__Tz3HQ')
    last_markdown_container = all_markdown_containers[-1]
    last_answer = last_markdown_container.text
    last_score = min([int(num) for num in re.findall(r'\d+', last_answer)])
    Q3_answer_list.append(last_answer)
    Q3_score_list.append(last_score)

column_names = ["Q1_LITERAL_Answer", "Q1_LITERAL_Score", "Q1_METAPHORICAL_Answer", "Q1_METAPHORICAL_Score",
                "Q2_LITERAL_Answer", "Q2_LITERAL_Score", "Q2_METAPHORICAL_Answer", "Q2_METAPHORICAL_Score",
                "Q3_Answer", "Q3_Score"]

data_lists = [Q1_answer_list, Q1_score_list, Q1_2_answer_list, Q1_2_score_list,
              Q2_answer_list, Q2_score_list, Q2_2_answer_list, Q2_2_score_list,
              Q3_answer_list, Q3_score_list]

df = pd.DataFrame(data_lists).T
df.columns = column_names

df.to_excel('output.xlsx', index=False)
print("===> End. Results Saved in output.xlsx.")
input("Press Enter to exit...")
sys.exit()