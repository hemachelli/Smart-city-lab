import smtplib

# Your credentials - CHANGE THESE!
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # 16 chars, no spaces

def test_login():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        print("Connecting to Gmail...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        print("✅ SUCCESS: Login successful!")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    test_login()