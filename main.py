import os
import sys
import time
import csv
import traceback
from app.aj_driver import get_driver

VERSION = "1.0.1"

# Only import messagebox when needed
def show_gui_error(message):
    try:
        import tkinter
        from tkinter import messagebox
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("ENGINE_AJ Error", message)
    except Exception:
        pass  # fail silently if tkinter unavailable

def get_recipients():
    try:
        # Prompt for CSV file location (GUI file picker)
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        csv_path = filedialog.askopenfilename(
            title="Select recipients.csv file",
            filetypes=[("CSV files", "*.csv")],
        )
    except Exception as e:
        show_gui_error(f"Failed to open file dialog: {e}")
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
    print("\n❤️ Made With REAL Love ©2025 Richard Knowles")
    print("🌠 GitHub: https://github.com/richknowles/ENGINE_AJ")
    print(f"🔖 Version: {VERSION}")
    print("📄 Licensed under GPL-3.0-or-later — because love shouldn't have NDAs.\n")

def main():
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
        print("📤 Sending messages... (TODO: message sending logic goes here)")

        # for number in recipients:
        #     send_whatsapp_message(driver, number, "Hello from ENGINE_AJ!")

    except Exception as e:
        error_text = f"❌ Unexpected error: {e}\n\n{traceback.format_exc()}"
        print(error_text)
        show_gui_error(error_text)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_gui_error(f"Fatal error:\n{e}")