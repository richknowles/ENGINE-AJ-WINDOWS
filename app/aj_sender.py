from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from app.aj_utils import human_delay, simulate_mouse_scroll
import time

def send_message(driver, number, message):
    url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
    print(f"🌐 Navigating to {url}")
    driver.get(url)
    human_delay(6, 9)
    simulate_mouse_scroll(driver)

    try:
        print("🔎 Waiting for message input box...")
        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]'))
        )
        print("✍️ Preparing to send message...")

        try:
            send_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(send_btn).pause(0.5).click().perform()
        except Exception:
            print("❗Send button not found or not clickable. Falling back to pressing RETURN.")
            input_box.send_keys(Keys.RETURN)

        human_delay(2, 3)
        print(f"✅ Sent message to {number}")

    except Exception as e:
        print("⚠️ Timeout or failure detected.")
        print(f"📍 Page title: {driver.title}")
        print(f"📍 Current URL: {driver.current_url}")
        screenshot_path = f"screenshot_error_{number}.png"
        driver.save_screenshot(screenshot_path)
        print(f"🖼️ Screenshot saved: {screenshot_path}")
        print(f"❌ Error sending to {number}: {type(e).__name__}: {e}")
