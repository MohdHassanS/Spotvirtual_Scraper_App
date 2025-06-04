# 📊 SpotVirtual Member Name Scraper

A **Streamlit web app** that automates login to [SpotVirtual](https://spotvirtual.com/), verifies with OTP, and **scrapes attendee names** from a virtual space using **Selenium**. Easily view who's present — minus the noise (zones, rooms, etc).

---

## 🚀 Features

- 🔐 Secure login with OTP
- 🔁 Re-scrape attendees anytime
- 🧠 Persistent login using Streamlit’s session state
- 🧹 Removes unwanted noise (zones, rooms)
- 🌐 Deployable on Azure VM, Render, or any Streamlit-supported platform

---

## 📦 Tech Stack

| Layer              | Technology          |
|--------------------|---------------------|
| UI Framework       | Streamlit           |
| Web Automation     | Selenium            |
| Browser Drivers    | ChromeDriver        |
| Package Handling   | WebDriver Manager   |
| Python Version     | 3.8+                |

---

## ⚙️ Deployment: Run on Azure VM (Ubuntu)

## ✅ Prerequisites
- Azure Ubuntu VM with a public IP
- GitHub repo of this app
- SSH access (using Azure CLI or key)
- Python 3.8+

---

## 🧱 Step 1: Connect to Azure VM using SSH using Azure CLI

```bash
az ssh vm --resource-group <RESOURCE_GROUP> --vm-name <VM_NAME> --subscription <SUBSCRIPTION_ID>
```

---

## 🐍 Step 2: Set up Python Environment

```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
python3 -m venv scraper-env
. scraper-env/bin/activate  # For Azure CLI, use '.' instead of 'source'
```

---

## 🛠️ Step 3: Clone the Repo and Install Requirements

```bash
git clone https://github.com/MohdHassanS/Spotvirtual_Scraper_App.git

# (Optional) Ensure you're on the latest commit of main branch
git checkout main
git pull origin main

cd Spotvirtual_Scraper_App
pip install -r requirements.txt
```

---

## 🌐 Step 4: Install Chromium + ChromeDriver

```bash
sudo apt install chromium-browser chromium-chromedriver -y

# Recommended (if Chromium causes headless issues)
# Note: On headless VMs, Google Chrome is often more stable than Snap-based Chromium.
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

Ensure both are installed:

```bash
google-chrome --version && chromium-browser --version && chromedriver --version
which google-chrome && which chromium-browser && which chromedriver
```

---

## 🧪 Step 5: Test Locally

```bash
streamlit run spot.py
```

Access the app at:  
- `http://localhost:8501`
- `http://<your-vm-public-ip>:8501`

---

## 🕒 Step 6: Set Up Cron Job to Start/Stop App on Schedule

```bash
crontab -e
```

Add the following lines (adjust paths and times as needed):

```bash
# Start Streamlit at 8:45 AM IST (3:15 UTC)
15 3 * * * cd /home/mohammedhassanmiet/Spotvirtual_Scraper_App && /home/mohammedhassanmiet/scraper-env/bin/python3 -m streamlit run spot.py --server.address=0.0.0.0 > /home/mohammedhassanmiet/streamlit.log 2>&1 &

# Stop Streamlit at 10:30 AM IST (5:00 UTC)
0 5 * * * pkill -f streamlit
```

To verify it's running:

```bash
ps aux | grep streamlit
```

---

## 🌐 Step 7: Access Your App

Open your browser and visit:

👉 **http://<IP_ADDRESS>:8501**

---

## 🔒 Step 8 (Optional): Secure with HTTPS

If you link your IP to a domain (e.g., `app.yourdomain.com`), you can use **Certbot + Nginx** to get free HTTPS. Ask me for a detailed guide when you're ready.

---

## ✅ Deployment Complete

You now have:
- A Streamlit app live and automated with `cron`
- Chromium and ChromeDriver installed for Selenium use
- The app starts and stops based on your schedule


## 📄 Project Structure

```
📁 Spotvirtual_Scraper_App/
├── spot.py               # Main Streamlit app
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── scraper-env/          # Python virtual environment (not pushed to GitHub)
```

---

## 🧪 Sample Screens

Here are some screenshots of the Streamlit app in action:


### 🔐 Login with mail
![Streamlit App Screenshot](./Streamlit_working_Screenshots/WhatsApp%20Image%202025-06-04%20at%2012.08.42_2011da95.jpg)

### 🔐 OTP Verification
![Login Screenshot](./Streamlit_working_Screenshots/WhatsApp%20Image%202025-06-04%20at%2012.09.28_5ec237ac.jpg)

### 📋 confirming the OTP
![Scraped Data Screenshot](./Streamlit_working_Screenshots/WhatsApp%20Image%202025-06-04%20at%2012.10.17_e03121db.jpg)

### ✅ Scrapping...  
![Cleaned Output Screenshot](./Streamlit_working_Screenshots/WhatsApp%20Image%202025-06-04%20at%2012.10.53_26a4cf6b.jpg)

### 📊 Diplaying the Scrapped Data  
![Extra Screenshot](./Streamlit_working_Screenshots/WhatsApp%20Image%202025-06-04%20at%2012.11.26_6012d2bc.jpg)

---

## 🙏 Acknowledgements

- Thanks to the [SpotVirtual](https://spotvirtual.com) team
- Streamlit + Selenium community for enabling fast prototyping

---

## ✍️ Author

**Mohammed Hassan**  
_Data Science Specialist @ Guvi_

---

## 📫 Contact

- 📧 Email: mohammedhassan.mech@gmail.com
- 🐙 GitHub: [MohdHassanS](https://github.com/MohdHassanS)
