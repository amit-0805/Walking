# 🚶 Walking - Google Fit Step Inserter

This Python script allows you to insert step count data into your Google Fit account using the Google Fitness API.

---

## 📦 Features

- Authenticate with your Google account.
- Insert custom step counts into your Google Fit timeline.
- Lightweight and easy to set up.

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Required Libraries

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 requests
```

---

## 🚀 Running the Script

```bash
python insert_steps.py
```

- This will open a browser window for Google login.
- **Use the Google account that is linked to Google Fit.**
- Upon login, authentication will complete, and the script will be ready to insert steps.

---

## ✍️ Set Your Step Count

Before running the script, **update the number of steps** in the two designated places inside the `insert_steps.py` file. These are usually variables like:

```python
step_count = 5000  # Update this with your desired step count
```

Make sure both locations are updated accordingly.

---

## ✅ Insert the Steps

After updating the values, re-run the script:

```bash
python insert_steps.py
```

You’re done! The specified number of steps will be added to your Google Fit account.

---
