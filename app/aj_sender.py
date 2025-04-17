
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.aj_utils import human_delay, simulate_mouse_scroll
import pyautogui
import time
import random
import os

def send_message(driver, number, message):
    print(f"🌐 Navigating to https://web.whatsapp.com/send?phone={number}&text={message}")
    driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")
    human_delay(8, 12)
    simulate_mouse_scroll(driver)

    try:
        print("🕵️ Checking login state...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//canvas[contains(@aria-label, "Scan me!")]'))
        )
        print("📵 Not logged in (QR code detected).")
        return
    except:
        print("✅ Logged into WhatsApp.")

    try:
        print("🔎 Waiting for input box using new XPath (up to 45s)...")
        input_box = WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
        )
        print("✅ Input box found.")

        try:
            send_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
            )
            print("🎯 Send button found.")

            try:
                print("🧪 JS click attempt...")
                driver.execute_script("arguments[0].click();", send_btn)
                time.sleep(1)
                post_input = driver.find_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')
                if post_input.text.strip() == "":
                    print(f"✅ Message confirmed sent to {number} via JS.")
                    return
                else:
                    print("⚠️ Message still present after JS click.")
            except Exception as js_error:
                print(f"❌ JS click failed: {js_error}")

            print("🖱️ pyautogui fallback...")
            window_position = driver.get_window_position()
            location = send_btn.location_once_scrolled_into_view
            size = send_btn.size
            x = location['x'] + size['width'] // 2 + window_position['x']
            y = location['y'] + size['height'] // 2 + window_position['y']

            pyautogui.moveTo(x, y, duration=random.uniform(0.8, 1.3))
            pyautogui.click()
            time.sleep(1)

            post_input = driver.find_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')
            if post_input.text.strip() == "":
                print(f"✅ Message confirmed sent to {number} via pyautogui.")
                return
            else:
                print("⚠️ Message still present after pyautogui click.")

        except Exception as e:
            print(f"❌ Send button error: {e}")

        print("⏎ ENTER fallback...")
        input_box.send_keys(Keys.RETURN)
        time.sleep(1)
        post_input = driver.find_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')
        if post_input.text.strip() == "":
            print(f"✅ Message confirmed sent to {number} via RETURN.")
        else:
            print(f"❌ Message still not sent to {number} after all fallbacks.")

    except Exception as fail:
        print("🧨 Could not locate input box. Saving screenshot...")
        try:
            os.makedirs("debugshots", exist_ok=True)
            filename = f"debugshots/fail_{number}_{int(time.time())}.png"
            driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as ss_err:
            print(f"📷 Screenshot failed: {ss_err}")
        print(f"❌ Final error: {type(fail).__name__}: {fail}")
