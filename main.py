import os
import sys
import time
import csv
import tkinter as tk
from tkinter import filedialog
from app.aj_driver import get_driver

VERSION = "1.0.2"

def get_recipients():
    root = tk.Tk()
    root.withdraw()
    print("📂 Please select your recipients.csv file...")
    csv_path = filedialog.askopenfilename(
        title="Select recipients.csv file",
        filetypes=[("CSV files", "*.csv")],
    )
    if not csv_path:
        print("❌ No file selected.")
        return []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            return [row[0].strip() for row in reader if row]
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
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
        print("⚠️ No phone numbers loaded. Exiting.")
        input("Press ENTER to close.")
        return

    print(f"📨 Loaded {len(recipients)} recipient(s).")
    print("🚀 Launching WhatsApp Automation Engine...")

    try:
        driver = get_driver()
        print("✅ Browser launched successfully. Scan QR code if needed.")
        time.sleep(60)
        print("✅ WhatsApp Web should now be ready.")
        print("📤 Sending messages... (TODO: message sending logic goes here)")
    except Exception as e:
        print(f"❌ Error: {e}")

    input("✅ Done. Press ENTER to exit.")

if __name__ == "__main__":
    main()
