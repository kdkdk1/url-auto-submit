import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- CONFIG ----------------
PANEL_URL = "https://personal-fast-index.info/panel20/panel.php"   # 🔴 CHANGE THIS

USERNAME = os.getenv("PANEL_USER")
PASSWORD = os.getenv("PANEL_PASS")

URLS = [
    "https://example1.com",
    "https://example2.com"
]

# ---------------- DRIVER SETUP ----------------
def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    )

    driver = webdriver.Chrome(service=service, options=options)
    return driver

# ---------------- MAIN BOT ----------------
def run():
    logging.info("🚀 Starting bot")

    driver = setup_driver()

    try:
        driver.get(PANEL_URL)
        time.sleep(3)

        # ---------------- LOGIN ----------------
        logging.info("🔐 Logging in...")

        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button").click()

        time.sleep(5)

        logging.info("✅ Login done")

        # ---------------- URL INPUT ----------------
        logging.info(f"📥 Submitting {len(URLS)} URLs")

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        textarea.clear()
        textarea.send_keys("\n".join(URLS))

        time.sleep(2)

        # ---------------- SUBMIT ----------------
        logging.info("📤 Clicking submit button")

        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Import')]")
        submit_btn.click()

        time.sleep(5)

        logging.info("🎉 Submission attempt done")

        driver.save_screenshot("success.png")

    except Exception as e:
        logging.error(f"❌ Error: {e}")
        driver.save_screenshot("error.png")

    finally:
        driver.quit()
        logging.info("✨ Finished")

if __name__ == "__main__":
    run()
