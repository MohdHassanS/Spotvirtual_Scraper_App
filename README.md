# 📊 SpotVirtual Member Name Scraper

A **Streamlit web app** that automates login to [SpotVirtual](https://spotvirtual.com/), verifies with OTP, and **scrapes attendee names** from a virtual space using **Selenium**. Easily view who's present — minus the noise (zones, rooms, etc).

---

## 🚀 Features

- 🔐 **OTP-based secure login**
- 🧠 **Session state** management to keep your login intact across app actions
- 🧹 Filters out unwanted zone/room names — gives you **clean, readable attendee names**
- 🔁 Re-scrape anytime without restarting the app
- 🌐 Deployable on **Render** or any Streamlit-supported platform

---

## 📦 Tech Stack

| Component        | Technology     |
|------------------|----------------|
| Frontend UI      | Streamlit      |
| Web Automation   | Selenium       |
| Driver Handling  | WebDriver Manager |
| Python Version   | 3.8+           |

---

## ⚙️ Setup & Deployment

### 🔧 Local Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/spotvirtual-scraper.git
   cd spotvirtual-scraper
   ```

2. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Streamlit App**
   ```bash
   streamlit run spot.py
   ```

### 🌐 Deploy on Render

1. Create a new **Render Web Service**
2. Connect your GitHub repo
3. Set **Start Command** to:
   ```bash
   streamlit run spot.py --server.port=10000 --server.address=0.0.0.0
   ```
4. Set **Python Version** in `render.yaml` or environment:
   ```yaml
   build:
     pythonVersion: "3.10"
   ```

---

## 📄 Project Structure

```
📁 spotvirtual-scraper/
├── spot.py               # Main Streamlit app
├── requirements.txt     # All dependencies
└── README.md            # This file
```

---

## 🧪 Sample Screens

![Sample UI](https://i.imgur.com/YOUR_IMAGE_URL.png)

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

- 📧 Email: mohammedhassan.mechgmail.com
- 🐙 GitHub: [github.com/your-username](https://github.com/MohdHassanS)
