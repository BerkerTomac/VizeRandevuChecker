import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from whatsapp_notifier import send_whatsapp_message
from config import VISA_URL, CHECK_INTERVAL

class VisaChecker:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        self.driver = webdriver.Chrome(options=options)

    def check_availability(self):
        try:
            self.driver.get(VISA_URL)
            appointment_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "appointment-slots"))
            )
            
            available_dates = appointment_element.find_elements(By.CLASS_NAME, "available-slot")
            
            if available_dates:
                dates_text = [date.text for date in available_dates]
                return True, dates_text
            return False, []
            
        except Exception as e:
            print(f"Error checking availability: {e}")
            return False, []

    def run(self):
        while True:
            available, dates = self.check_availability()
            if available:
                message = f"Visa appointment available for the following dates:\n{', '.join(dates)}"
                send_whatsapp_message(message)
                print(message)
            
            time.sleep(CHECK_INTERVAL)

    def __del__(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    checker = VisaChecker()
    checker.run() 