import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from io import BytesIO
import traceback
import time
import re
import os

# --- Streamlit App ---
st.set_page_config(page_title="SpotVirtual Scraper", layout="centered")
st.title("👥 Hey Guvi'ans! Let see who was there with us in the SpotVirtual....!! ")

if 'driver' not in st.session_state:
    with st.spinner("Wait for it...", show_time=True):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # critical for low-shm environments
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--remote-debugging-port=9222")
        options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")
        
        driver = webdriver.Chrome(options=options)
        st.session_state.driver = driver

        
def send_code_to_email(email,driver=st.session_state.driver):
    with st.spinner("Wait for it...", show_time=True):
        driver.get("https://spotvirtual.com/login")
        time.sleep(5)

        email_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='Input_inputContainer__dDsj- Input_lg__Aj82U Input_border__mGsTY']//input")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        st.session_state.opt = True

def confirm_verification_code(code, driver=st.session_state.driver):
    try:
        with st.spinner("Wait for it...", show_time=True):
            code_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class, 'ConfirmCodeInput_self')]//input")))
            code = re.sub(r'[^a-zA-Z0-9]', '', code)
            for i, digit in enumerate(code):
                code_inputs[i].send_keys(digit)
            time.sleep(5)
            st.session_state.login = 'success'
            st.success("verified the code .. Entered the spot Successfully")
            

    except Exception as e:
        st.error(f"An error occurred : ")
        error_details = traceback.format_exc()
        st.code(error_details, language='python')
        st.session_state.code = ''
        st.session_state.email = ''
        st.session_state.opt = False
        del st.session_state.driver
        driver.quit()
        st.button('Rerun')

def scrape_names(driver=st.session_state.driver):
    with st.spinner("Wait for it...", show_time=True):
        time.sleep(5)
        screenshot = driver.get_screenshot_as_png()
        st.image(BytesIO(screenshot), caption='before scraping')
        element = driver.find_elements(By.XPATH, "//div[contains(@class, 'OrgSidebar_scrollContainer')]")
        text_content = "\n".join([el.text for el in element])
        spliting = list(set(text_content.splitlines()))
        if "ADMIN" in spliting:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[5]//div[2]//a[1]"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[6]//div[2]//a[1]"))).click()
        else:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[4]//div[2]//a[1]"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[5]//div[2]//a[1]"))).click()
        # for xpath in ["//div[4]//div[2]//a[1]","//div[5]//div[2]//a[1]","//div[6]//div[2]//a[1]"]:
        #     try:
        #         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,xpath))).click()
        #         st.write(xpath)
        #     except:
        #         st.write('missed')
        #         pass
        element = driver.find_elements(By.XPATH, "//div[contains(@class, 'OrgSidebar_scrollContainer')]")
        text_content = "\n".join([el.text for el in element])
        spliting = list(set(text_content.splitlines()))
        unwanted = ['Browse channels','Browse spaces',"You haven't joined any channels",'GUESTS','Office',' Invite teammates','MEMBERS','SPACES','CHANNELS','Show less','ADMIN']
        cleaned = sorted([i for i in spliting if len(i)>2 and i not in unwanted])
        return cleaned

if 'email' not in st.session_state:
    st.session_state.email = ''

if 'code' not in st.session_state:
    st.session_state.code = ''

if 'opt' not in st.session_state:
    st.session_state.opt = False

if 'login' not in st.session_state:
    st.session_state.login = ''

if st.session_state.email =='' and st.session_state.opt == False:
    if st.session_state.login == '':
        st.warning("Reload the page entirely ... if you face any Technical Errors")
        st.text_input("Enter your SpotVirtual email or office mail id",key='email')

if st.session_state.email !='' and st.session_state.opt == False:
    send_code_to_email(st.session_state.email)
    st.success("OTP sent to your email. Now enter the code below.")

if st.session_state.code =='' and st.session_state.opt:
    if st.session_state.login == '':
        st.text_input("Enter the code",key="code")

if st.session_state.code !='' and st.session_state.opt:
    confirm_verification_code(st.session_state.code)

if st.session_state.login == 'success' and st.button("Scrape Data"):
    attendees = scrape_names()
    st.write("Total Presentees  : ",len(attendees))
    st.write("Presentees Name :   ",','.join(attendees))
    st.write(attendees)

