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
            try:
                st.session_state.driver.quit()
            except:
                pass
        for key in list(st.session_state.keys()):
            del st.session_state[key]

def create_chrome_driver():
    """Create Chrome driver with maximum stability for server environments"""
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
    
    # Try different approaches to create the driver
    driver = None
    
    # Method 1: Try with Google Chrome stable (after installation)
    chrome_paths = [
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/opt/google/chrome/chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium"
    ]
    
    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            try:
                st.info(f"Found Chrome at: {chrome_path}")
                options.binary_location = chrome_path
                
                # Try with webdriver-manager first
                try:
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)
                    st.success(f"✅ Driver created successfully with {chrome_path} + webdriver-manager!")
                    return driver
                except Exception as e:
                    st.warning(f"webdriver-manager failed with {chrome_path}: {str(e)}")
                
                # Try with system chromedriver
                chromedriver_paths = [
                    "/usr/bin/chromedriver",
                    "/usr/local/bin/chromedriver",
                    "/snap/bin/chromium.chromedriver"
                ]
                
                for driver_path in chromedriver_paths:
                    if os.path.exists(driver_path):
                        try:
                            st.info(f"Trying ChromeDriver at: {driver_path}")
                            service = Service(driver_path)
                            driver = webdriver.Chrome(service=service, options=options)
                            st.success(f"✅ Driver created successfully with {chrome_path} + {driver_path}!")
                            return driver
                        except Exception as e:
                            st.warning(f"Failed with {driver_path}: {str(e)}")
                            continue
                
            except Exception as e:
                st.warning(f"Failed with Chrome at {chrome_path}: {str(e)}")
                continue
    
    # Method 2: Try with default service (last resort)
    try:
        st.info("Trying with default service...")
        options.binary_location = ""  # Let selenium find Chrome
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        st.success("✅ Driver created successfully with default service!")
        return driver
    except Exception as e:
        st.error(f"Default service failed: {str(e)}")
    
    return None

def ensure_driver_alive():
    """Check if driver is alive and recreate if needed"""
    if 'driver' not in st.session_state:
        return False
    
    try:
        # Test if driver is responsive
        st.session_state.driver.current_url
        return True
    except Exception as e:
        st.warning(f"Driver connection lost: {str(e)}")
        try:
            st.session_state.driver.quit()
        except:
            pass
        del st.session_state.driver
        return False

def get_or_create_driver():
    """Get existing driver or create new one if needed"""
    if not ensure_driver_alive():
        st.info("Recreating browser connection...")
        with st.spinner("Reconnecting to browser...", show_time=True):
            driver = create_chrome_driver()
            if driver is None:
                st.error("❌ Failed to create browser connection")
                return None
            st.session_state.driver = driver
            st.success("✅ Browser reconnected successfully!")
    
    return st.session_state.driver
if 'driver' not in st.session_state:
    get_or_create_driver()

def send_code_to_email(email, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver = get_or_create_driver()
            if driver is None:
                st.error("Cannot establish browser connection")
                return False
                
            with st.spinner(f"Sending verification code... (Attempt {attempt + 1}/{max_retries})", show_time=True):
                driver.get("https://spotvirtual.com/login")
                
                # Wait for page to load completely
                time.sleep(8)
                
                # Try multiple selectors for email input
                email_selectors = [
                    "//div[@class='Input_inputContainer__dDsj- Input_lg__Aj82U Input_border__mGsTY']//input",
                    "//input[@type='email']",
                    "//input[contains(@placeholder, 'email')]",
                    "//input[contains(@class, 'Input')]"
                ]
                
                email_input = None
                for selector in email_selectors:
                    try:
                        email_input = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                
                if email_input is None:
                    raise Exception("Could not find email input field")
                
                # Clear and enter email
                email_input.clear()
                time.sleep(1)
                email_input.send_keys(email)
                time.sleep(2)
                email_input.send_keys(Keys.RETURN)
                
                # Wait for response
                time.sleep(5)
                
                st.session_state.opt = True
                st.success("✅ Verification code sent successfully!")
                return True
                
        except Exception as e:
            st.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                st.info("Retrying...")
                time.sleep(3)
            else:
                st.error("Failed to send verification code after all attempts")
                error_details = traceback.format_exc()
                st.code(error_details, language='python')
                # Don't delete driver, just mark as failed
                return False
    
    return False

def confirm_verification_code(code, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver = get_or_create_driver()
            if driver is None:
                st.error("Cannot establish browser connection")
                return False
                
            with st.spinner(f"Verifying code... (Attempt {attempt + 1}/{max_retries})", show_time=True):
                # Clean the code
                code = re.sub(r'[^a-zA-Z0-9]', '', code)
                
                # Try multiple selectors for code inputs
                code_selectors = [
                    "//div[contains(@class, 'ConfirmCodeInput_self')]//input",
                    "//input[@type='text']",
                    "//input[contains(@class, 'code')]"
                ]
                
                code_inputs = None
                for selector in code_selectors:
                    try:
                        code_inputs = WebDriverWait(driver, 15).until(
                            EC.presence_of_all_elements_located((By.XPATH, selector))
                        )
                        if len(code_inputs) >= len(code):
                            break
                    except:
                        continue
                
                if code_inputs is None or len(code_inputs) < len(code):
                    raise Exception("Could not find verification code input fields")
                
                # Enter code digits
                for i, digit in enumerate(code):
                    if i < len(code_inputs):
                        code_inputs[i].clear()
                        time.sleep(0.5)
                        code_inputs[i].send_keys(digit)
                        time.sleep(0.5)
                
                # Wait for verification
                time.sleep(8)
                
                st.session_state.login = 'success'
                st.success("✅ Code verified successfully! Entered SpotVirtual.")
                return True
                
        except Exception as e:
            st.warning(f"Verification attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                st.info("Retrying verification...")
                time.sleep(3)
            else:
                st.error("Failed to verify code after all attempts")
                error_details = traceback.format_exc()
                st.code(error_details, language='python')
                return False
    
    return False

def scrape_names(max_retries=3):
    for attempt in range(max_retries):
        try:
            driver = get_or_create_driver()
            if driver is None:
                st.error("Cannot establish browser connection")
                return []
                
            with st.spinner(f"Scraping attendee data... (Attempt {attempt + 1}/{max_retries})", show_time=True):
                time.sleep(5)

                # Try to click "Show all" buttons with retries
                try:
                    show_all_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Show all"))
                    )
                    show_all_button.click()
                    st.info("Clicked 'Show all' button (1)")
                    time.sleep(3)
                    
                    try:
                        show_all_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.LINK_TEXT, "Show all"))
                        )
                        show_all_button.click()
                        st.info("Clicked 'Show all' button (2)")
                        time.sleep(3)
                    except:
                        st.info("Second 'Show all' button not found - proceeding")
                        
                except: 
                    st.info("'Show all' buttons not found - proceeding with available data")

                # Scrape the sidebar with multiple selector attempts
                sidebar_selectors = [
                    "Sidebar_sidebar__olcdO",
                    "sidebar",
                    "[class*='sidebar']",
                    "[class*='Sidebar']"
                ]
                
                sidebar = None
                for selector in sidebar_selectors:
                    try:
                        if selector.startswith('['):
                            sidebar = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                            )
                        else:
                            sidebar = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, selector))
                            )
                        break
                    except:
                        continue
                
                if sidebar is None:
                    raise Exception("Could not find sidebar element")
                
                sidebar_text = sidebar.text
                spt = sidebar_text.splitlines()
                
                # Filter out unwanted entries
                unwanted = [
                    'New ZEN DS', 'Browse spaces', 'Browse channels', 
                    "You haven't joined any channels", 'GUESTS', 'Office', 
                    ' Invite teammates', 'MEMBERS', 'SPACES', 'CHANNELS', 
                    'Show less', 'ADMIN', 'Show all', 'Settings', 'Help',
                    'Logout', 'Profile', 'Notifications'
                ]
                
                cleaned_names = sorted([
                    name.strip() for name in spt 
                    if len(name.strip()) > 2 and name.strip() not in unwanted and not name.strip().isdigit()
                ])
                
                if cleaned_names:
                    return cleaned_names
                else:
                    raise Exception("No attendee names found")
                
        except Exception as e:
            st.warning(f"Scraping attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                st.info("Retrying data scraping...")
                time.sleep(5)
            else:
                st.error("Failed to scrape data after all attempts")
                error_details = traceback.format_exc()
                st.code(error_details, language='python')
                return []
    
    return []

# Initialize session state variables
for key, default_value in [
    ('email', ''),
    ('code', ''),
    ('opt', False),
    ('login', '')
]:
    if key not in st.session_state:
        st.session_state[key] = default_value

# Main application flow
if st.session_state.email == '' and not st.session_state.opt:
    if st.session_state.login == '':
        st.warning("⚠️ Reload the page entirely if you face any technical errors")
        st.text_input("Enter your SpotVirtual email or office mail ID:", key='email')

if st.session_state.email != '' and not st.session_state.opt:
    if send_code_to_email(st.session_state.email):
        st.success("📧 OTP sent to your email. Enter the verification code below.")
    else:
        st.error("Failed to send OTP. Please try refreshing the page.")

if st.session_state.code == '' and st.session_state.opt:
    if st.session_state.login == '':
        st.text_input("Enter the verification code:", key="code")

if st.session_state.code != '' and st.session_state.opt:
    if st.session_state.login != 'success':
        confirm_verification_code(st.session_state.code)

if st.session_state.login == 'success' and st.button("🔍 Scrape Attendee Data"):
    attendees = scrape_names()
    if attendees:
        st.success(f"✅ Successfully scraped {len(attendees)} attendees!")
        st.write("**Total Attendees:**", len(attendees))
        st.write("**Attendee Names:**", ', '.join(attendees))
        
        # Display as a nice list
        st.write("**Detailed List:**")
        for i, name in enumerate(attendees, 1):
            st.write(f"{i}. {name}")
    else:
        st.warning("No attendee data found. Please check if you're logged in correctly.")