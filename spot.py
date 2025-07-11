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

if st.button("Full Refresh"):
    if len(list(st.session_state.keys())) != 0:
        if 'driver' in st.session_state:
            st.session_state.driver.quit()
        for key in list(st.session_state.keys()):
            del st.session_state[key]


if 'driver' not in st.session_state:
    with st.spinner("Wait for it...", show_time=True):
        # Create Chrome driver with maximum stability for server environments
        options = Options()
        
        # Core stability options
        options.add_argument("--headless=new")  # Use new headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        
        # Browser stability and crash prevention
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-in-process-stack-traces")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-breakpad")
        
        # Memory and resource management
        options.add_argument("--memory-pressure-off")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
        
        # Network and security
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        
        # Rendering optimizations
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-gpu-rasterization")
        options.add_argument("--disable-gpu-sandbox")
        options.add_argument("--window-size=1280,720")  # Smaller window
        
        # Process management - try without single-process first
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Experimental options for stability
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Page load strategy for faster loading
        options.page_load_strategy = 'eager'

        options.binary_location = "/usr/bin/google-chrome"

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        st.session_state.driver = driver

        
def send_code_to_email(email,driver=st.session_state.driver):
    with st.spinner("Sending verification code...", show_time=True):
        driver.get("https://spotvirtual.com/login")
        time.sleep(5)

        email_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='Input_inputContainer__dDsj- Input_lg__Aj82U Input_border__mGsTY']//input")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        st.session_state.opt = True

def confirm_verification_code(code, driver=st.session_state.driver):
    try:
        with st.spinner("Verifying code...", show_time=True):
            code_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class, 'ConfirmCodeInput_self')]//input")))
            code = re.sub(r'[^a-zA-Z0-9]', '', code)
            for i, digit in enumerate(code):
                code_inputs[i].send_keys(digit)
            time.sleep(5)
            st.session_state.login = 'success'
            st.success("✅ Code verified successfully! Entered SpotVirtual.")
            

    except Exception as e:
        st.error(f"An error occurred : ")
        error_details = traceback.format_exc()
        st.code(error_details, language='python')
        st.session_state.driver.quit()
        for key in list(st.session_state.keys()):
            del st.session_state[key]

def scrape_names(driver=st.session_state.driver):
    with st.spinner("Scraping...",show_time=True):
        time.sleep(3)

        try:
            show_all_button = driver.find_element(By.LINK_TEXT, "Show all")
            show_all_button.click()
            st.write("Found Show all 1")
            time.sleep(3)
            show_all_button = driver.find_element(By.LINK_TEXT, "Show all")
            show_all_button.click()
            st.write("Found Show all 2")
        except: 
            st.write("Not Found Show all")

        try:
            sidebar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "Sidebar_sidebar__olcdO")))
            sidebar_text = sidebar.text
            spt = sidebar_text.splitlines()
            unnes = ['New ZEN DS','Browse spaces','Browse channels',"You haven't joined any channels",'GUESTS','Office',' Invite teammates','MEMBERS','SPACES','CHANNELS','Show less','ADMIN']
            cln = sorted([i for i in spt if len(i)>2 and i not in unnes])
            return cln
        except:
            st.error(f"An error occurred : ")
            error_details = traceback.format_exc()
            st.code(error_details, language='python')
            return []

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
        st.warning("Reload the page entirely/Click  Full refresh... if you face any Technical Errors")
        st.text_input("Enter your SpotVirtual email or office mail id",key='email')

if st.session_state.email !='' and st.session_state.opt == False:
    send_code_to_email(st.session_state.email)
    st.success("✅ Verification code sent successfully to your email ! Now check and enter the code below.")

if st.session_state.code =='' and st.session_state.opt:
    if st.session_state.login == '':
        st.text_input("Enter the code",key="code")

if st.session_state.code !='' and st.session_state.opt:
    confirm_verification_code(st.session_state.code)

if st.session_state.login == 'success' and st.button("🔍 Scrape Attendee Data"):
    attendees = scrape_names()
    if attendees:
        st.success(f"✅ Successfully scraped {len(attendees)} attendees!")
        st.write("**Attendee Names:**", ', '.join(attendees))
        
        # Display as a nice list
        st.write("**Detailed List:**")
        for i, name in enumerate(attendees, 1):
            st.write(f"{i}. {name}")
    else:
        st.warning("No attendee data found. Please check if you're logged in correctly.")
