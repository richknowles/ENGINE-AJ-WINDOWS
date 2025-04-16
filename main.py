
import tkinter as tk
from PIL import Image, ImageTk
import threading

def show_splash(image_path, duration=3000):
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    splash_root.configure(bg='black')

    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    image = Image.open(image_path)
    image = image.resize((512, 512), Image.Resampling.LANCZOS)
    splash_img = ImageTk.PhotoImage(image)

    splash_label = tk.Label(splash_root, image=splash_img, bg='black')
    splash_label.image = splash_img  # Keep reference
    splash_label.pack()

    x = (screen_width // 2) - (512 // 2)
    y = (screen_height // 2) - (512 // 2)
    splash_root.geometry(f"+{x}+{y}")

    def close_splash():
        splash_root.destroy()

    splash_root.after(duration, close_splash)
    threading.Thread(target=splash_root.mainloop).start()

# Show the splash screen
show_splash("aj_heart_splash.jpeg")

import os
import sys
import time
import csv
import traceback
from app.aj_driver import get_driver

VERSION = "1.0.4"

def show_gui_error(message):
    """Display a GUI error message using tkinter (fails silently if unavailable)."""
    try:
        import tkinter
        from tkinter import messagebox
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("ENGINE_AJ Error", message)
    except Exception:
        pass

def get_recipients():
    """Prompt user to select a recipients.csv file and load numbers."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        csv_path = filedialog.askopenfilename(
            title="Select recipients.csv file",
            filetypes=[("CSV files", "*.csv")],
        )
    except Exception as e:
        show_gui_error(f"Failed to open file dialog:\n{e}")
        return []

    if not csv_path or not os.path.exists(csv_path):
        show_gui_error("No recipients.csv file selected or file not found.")
        return []

    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row[0].strip() for row in reader if row]
    except Exception as e:
        show_gui_error(f"Failed to read CSV file:\n{e}")
        return []

def print_intro():
    """Prints the header and version info."""
    print("\n©2025 Richard Knowles")
    print("🌐 GitHub: https://github.com/richknowles/ENGINE_AJ")
    print(f"🛠️ Version: {VERSION}")
    print("📜 Licensed exclusively to Rich Knowles\n")

def send_whatsapp_message(driver, number, message):
    """Navigate to WhatsApp Web and send a message to a specific number."""
    try:
        url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
        driver.get(url)
        print(f"⏳ Sending to {number}...")
        time.sleep(10)  # Wait for WhatsApp to load the chat
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        input_box = driver.find_element(By.XPATH, '//div[@title="Type a message"]')
        input_box.send_keys(Keys.ENTER)
        print(f"✅ Message sent to {number}")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Failed to send message to {number}: {e}")

def main():
    """Main execution flow."""
    print_intro()

    recipients = get_recipients()
    if not recipients:
        print("⚠️ No phone numbers loaded.")
        return

    print(f"📨 Loaded {len(recipients)} recipient(s).")
    print("🚀 Launching WhatsApp Automation Engine...")

    try:
        driver = get_driver()
        print("✅ Browser launched successfully. Scan QR code if needed.")
        time.sleep(60)
        print("✅ WhatsApp Web should now be ready.")
        print("📤 Sending messages...")

        for number in recipients:
            send_whatsapp_message(driver, number, "Hello from ENGINE_AJ!")

    except Exception as e:
        error_text = f"❌ Unexpected error: {e}\n\n{traceback.format_exc()}"
        print(error_text)
        show_gui_error(error_text)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_gui_error(f"Fatal error:\n{e}")
