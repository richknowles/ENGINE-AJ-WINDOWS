
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.aj_utils import human_delay, simulate_mouse_scroll
import pyautogui
import time
import random
import os
import csv

metrics = {
    "total": 0,
    "sent": 0,
    "failed": 0,
    "screenshots": 0
}

log_rows = []

def send_message(driver, number, message):
    start_time = time.time()
    print(f"📨 Sending to: {number}")
    metrics["total"] += 1
    status = "FAILED"
    method = "N/A"

    try:
        driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")
        human_delay(8, 12)
        simulate_mouse_scroll(driver)

        print("🔎 Checking login state...")
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, '//canvas[contains(@aria-label, "Scan me!")]'))
            )
            print("📵 Not logged in (QR code found).")
            method = "Not logged in"
            raise Exception("Not logged in")
        except:
            print("✅ Logged in confirmed.")

        print("⌛ Looking for input box...")
        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
        )
        print("✅ Input box located.")

        try:
            send_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
            )
            print("🎯 Send button found.")

            try:
                driver.execute_script("arguments[0].click();", send_btn)
                time.sleep(1)
                post_input = driver.find_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')
                if post_input.text.strip() == "":
                    print(f"✅ Message sent via JavaScript")
                    method = "JavaScript"
                    status = "SUCCESS"
            except:
                print("⚠️ JS click failed, trying pyautogui...")

            if status != "SUCCESS":
                window_position = driver.get_window_position()
                location = send_btn.location_once_scrolled_into_view
                size = send_btn.size
                x = location['x'] + size['width'] // 2 + window_position['x']
                y = location['y'] + size['height'] // 2 + window_position['y']
                pyautogui.moveTo(x, y, duration=random.uniform(0.7, 1.2))
                pyautogui.click()
                time.sleep(1)
                post_input = driver.find_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')
                if post_input.text.strip() == "":
                    print(f"✅ Message sent via pyautogui")
                    method = "pyautogui"
                    status = "SUCCESS"
        except:
            print("❌ Send button not found or not clickable")

        if status != "SUCCESS":
            input_box.send_keys(Keys.RETURN)
            time.sleep(1)
            post_input = driver.find_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')
            if post_input.text.strip() == "":
                print(f"✅ Message sent via RETURN key")
                method = "RETURN"
                status = "SUCCESS"

    except Exception as fail:
        print(f"🧨 Exception occurred: {type(fail).__name__}: {fail}")
        try:
            os.makedirs("debugshots", exist_ok=True)
            filename = f"debugshots/fail_{number}_{int(time.time())}.png"
            driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
            metrics["screenshots"] += 1
        except:
            print("⚠️ Screenshot failed")

    duration = round(time.time() - start_time, 2)
    print(f"⏱ Took {duration}s")

    if status == "SUCCESS":
        metrics["sent"] += 1
        print(f"✅ Sent to {number} via {method}")
    else:
        metrics["failed"] += 1
        print(f"❌ Failed to send to {number}")

    print(f"📦 Progress: {metrics['sent'] + metrics['failed']}/{metrics['total']} processed")
    print("-" * 40)

    log_rows.append([number, status, method, f"{duration}s"])

def write_log_csv():
    with open("metrics_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Number", "Status", "Method", "Duration"])
        writer.writerows(log_rows)

def print_summary():
    print("📊 Summary:")
    print(f"   📬 Total numbers: {metrics['total']}")
    print(f"   ✅ Messages sent: {metrics['sent']}")
    print(f"   ❌ Failures: {metrics['failed']}")
    print(f"   📸 Screenshots saved: {metrics['screenshots']}")
    success_rate = round((metrics['sent'] / metrics['total']) * 100, 2) if metrics['total'] > 0 else 0
    print(f"   📈 Success rate: {success_rate}%")
    write_log_csv()
    print("📁 Log written to metrics_log.csv")
