import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
# --- Streamlit App ---
st.set_page_config(page_title="SpotVirtual Scraper", layout="centered")
st.title("👥 Hey Guvi'ans! Let see who was there with us in the SpotVirtual....!! ")

if 'driver' not in st.session_state:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    st.session_state.driver = driver

def send_code_to_email(email,driver=st.session_state.driver):
    driver.get("https://spotvirtual.com/login")
    time.sleep(5)

    email_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[@class='Input_inputContainer__dDsj- Input_lg__Aj82U Input_border__mGsTY']//input"
        ))
    )
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)
    # time.sleep(60)
    st.session_state.opt = True

def confirm_verification_code(code, driver=st.session_state.driver):
    try:
        code_inputs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((
            By.XPATH,
            "//div[contains(@class, 'ConfirmCodeInput_self')]//input"
        ))
    )
        code = re.sub(r'[^a-zA-Z0-9]', '', code)
        for i, digit in enumerate(code):
            code_inputs[i].send_keys(digit)
        time.sleep(5)
        for _ in range(3):
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='utils_d-flex__ngJ-O utils_gap-2xs__J5LwE']"))).click()
            time.sleep(2)
        st.session_state.login = 'success'
    except:
        st.session_state.code = ''
        st.session_state.email = ''
        st.session_state.opt = False
        del st.session_state.driver
        driver.quit()

        st.error("Incorrect OTP")
        st.rerun()

def scrape_names(driver=st.session_state.driver):

    for i in range(5):
        time.sleep(5)
        try:
            badge_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='Badge_badge__ZKvcA Badge_md__zbeVe Badge_muted__QtdpT Badge_isInteractable__3u2IK']"))
            )
            badge_button.click()
        except:
            break


    text = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='css-1hebf4y']"))
    ).text

    all_items = list(set(text.splitlines()))

    unwanted = ['Asst manager zone', 'Auditorium', 'BU Head Room', 'BU Head Zone', 'CAD Team', 'Collection zone', 
                'Data analyst zone', 'EMI Team', 'General Discussion Room', 'Hallway', 'KT zone', 'Leaders zone', 
                'Lounge', 'MBC CS', 'MBC Discussion Zone', 'MBC MA', 'MBC PA', 'MBC RT', 'MBC SC', 'MBC Tech zone', 
                'PBC Coordinators zone', 'PBC Interviewers zone', 'PC_1-1 meet room', 'PC_BADM(Eng)', 'PC_DS(Tam)', 
                'PC_Discussion Zone', 'PES Lead_zone', 'Payment Collection', 'Payments Audit', 'Payments-EMI', 
                'Placements CSE Room', 'Placements HR zone', 'Placements Tech zone', 'PreBoot Tech zone', 
                'Program Execution Head Zone', 'QC(Queries/Complaints)', 'Tech Head Zone', 'Tech discussion zone']

    for value in unwanted:
        try:
            all_items.remove(value)
        except:
            pass

    cleaned = sorted([i for i in all_items if len(i) > 2])
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


