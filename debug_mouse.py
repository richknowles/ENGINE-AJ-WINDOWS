
import pyautogui
import time
import sys

def log(msg):
    with open("debug_mouse_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(msg + "\n")
    print(msg)

log("🔧 DEBUG MOUSE SCRIPT STARTED")
try:
    # Check current position
    before = pyautogui.position()
    log(f"📍 Current mouse position: {before}")

    # Move to a known position on screen
    x_test, y_test = 300, 300
    log(f"➡️ Attempting to move to: ({x_test}, {y_test})")

    pyautogui.moveTo(x_test, y_test, duration=2)

    after = pyautogui.position()
    log(f"📍 New mouse position: {after}")

    if before == after:
        log("❌ Mouse did NOT move. pyautogui may be blocked by OS, RDP, or virtualization.")
    else:
        log("✅ Mouse moved successfully.")

except Exception as e:
    log(f"❌ Exception occurred: {type(e).__name__}: {e}")

log("🔚 DEBUG COMPLETE")
