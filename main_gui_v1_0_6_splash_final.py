
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
import time
import os
import csv
import sys
from app.aj_driver import get_driver
from app.aj_sender import send_message

VERSION = "v1.0.6"
REPO = "https://github.com/richknowles/ENGINE-AJ-WINDOWS"
COPYRIGHT = "©2025 Richard Knowles"

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(__file__)

def show_splash_then_start_gui():
    splash = tk.Tk()
    splash.overrideredirect(True)
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()

    image_path = os.path.join(BASE_PATH, "aj_heart_splash.jpeg")
    img = Image.open(image_path).resize((512, 512), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(splash, image=photo)
    label.image = photo
    label.pack()

    x = (screen_width - 512) // 2
    y = (screen_height - 512) // 2
    splash.geometry(f"512x512+{x}+{y}")
    splash.after(5000, splash.destroy)
    splash.mainloop()
    launch_gui()

def launch_gui():
    root = tk.Tk()
    root.title(f"ENGINE AJ {VERSION} – by Richard Knowles")
    root.geometry("700x500")

    file_path_var = tk.StringVar()
    message_text = tk.StringVar()

    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        file_path_var.set(file_path)

    def log(msg):
        log_output.insert(tk.END, msg + "\n")
        log_output.see(tk.END)

    def start_campaign():
        csv_path = file_path_var.get()
        msg = message_entry.get("1.0", tk.END).strip()

        if not os.path.exists(csv_path):
            messagebox.showerror("File Error", "CSV file not found.")
            return
        if not msg:
            messagebox.showerror("Input Error", "Message cannot be empty.")
            return

        numbers = []
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                numbers = [row[0].strip() for row in reader if row]
        except Exception as e:
            messagebox.showerror("CSV Error", f"Could not read CSV file:\n{e}")
            return

        driver = get_driver()
        for number in numbers:
            try:
                send_message(driver, number, msg)
                log(f"✅ Sent to {number}")
            except Exception as e:
                log(f"❌ Failed to send to {number}: {e}")
        driver.quit()

    tk.Label(root, text="Select recipients.csv:").pack(anchor='w', padx=10, pady=(10, 0))
    tk.Button(root, text="Browse", command=select_file).pack(padx=10, pady=5)
    tk.Label(root, textvariable=file_path_var, fg="blue").pack(anchor='w', padx=10)

    tk.Label(root, text="Message:").pack(anchor='w', padx=10, pady=(10, 0))
    message_entry = tk.Text(root, height=5, wrap=tk.WORD)
    message_entry.pack(fill='x', padx=10, pady=5)

    tk.Button(root, text="Start Campaign", bg="#f7768e", fg="white", command=start_campaign).pack(pady=10)

    log_output = scrolledtext.ScrolledText(root, height=10)
    log_output.pack(fill='both', expand=True, padx=10, pady=(5, 10))

    tk.Label(root, text=f"{COPYRIGHT} | {VERSION} | {REPO}", fg="gray").pack(side='bottom', pady=5)

    root.mainloop()

if __name__ == "__main__":
    try:
        show_splash_then_start_gui()
    except Exception as e:
        import traceback
        with open("crash_log.txt", "w", encoding="utf-8") as log_file:
            traceback.print_exc(file=log_file)
        raise
