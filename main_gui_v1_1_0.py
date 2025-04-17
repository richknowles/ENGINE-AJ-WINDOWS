
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

VERSION = "v1.1.0"
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

    image_path = os.path.join(BASE_PATH, "aj_heart_splash.png")
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
    root.title(f"ENGINE AJ {VERSION}")
    root.geometry("720x520")
    root.configure(bg="#1c1c1c")

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
                log(f"📤 Attempted to send to {number}")
            except Exception as e:
                log(f"❌ Failed to send to {number}: {e}")
        driver.quit()

    label_style = {"bg": "#1c1c1c", "fg": "#ff4d4d", "font": ("Segoe UI", 10, "bold")}
    entry_style = {"bg": "#2e2e2e", "fg": "white", "insertbackground": "white"}
    button_style = {"bg": "#ff4d4d", "fg": "white", "activebackground": "#cc0000"}

    tk.Label(root, text="Select recipients.csv:", **label_style).pack(anchor='w', padx=12, pady=(12, 0))
    tk.Button(root, text="Browse", command=select_file, **button_style).pack(padx=12, pady=5)
    tk.Label(root, textvariable=file_path_var, fg="#77ddff", bg="#1c1c1c", wraplength=680, justify="left").pack(anchor='w', padx=12)

    tk.Label(root, text="Message:", **label_style).pack(anchor='w', padx=12, pady=(12, 0))
    message_entry = tk.Text(root, height=5, wrap=tk.WORD, **entry_style)
    message_entry.pack(fill='x', padx=12, pady=5)

    tk.Button(root, text="Start Campaign", command=start_campaign, height=2, **button_style).pack(pady=12)

    log_output = scrolledtext.ScrolledText(root, height=10, bg="#1e1e1e", fg="white", insertbackground="white")
    log_output.pack(fill='both', expand=True, padx=12, pady=(5, 12))

    tk.Label(root, text=f"{COPYRIGHT} | {VERSION} | {REPO}", fg="#888888", bg="#1c1c1c", font=("Segoe UI", 8)).pack(side='bottom', pady=6)

    root.mainloop()

if __name__ == "__main__":
    try:
        show_splash_then_start_gui()
    except Exception as e:
        import traceback
        with open("crash_log.txt", "w", encoding="utf-8") as log_file:
            traceback.print_exc(file=log_file)
        raise
