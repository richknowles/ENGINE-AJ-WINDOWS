
import tkinter as tk
import pyautogui
import time

def create_overlay(x, y):
    overlay = tk.Tk()
    overlay.overrideredirect(True)
    overlay.geometry(f"20x20+{int(x)-10}+{int(y)-10}")
    overlay.wm_attributes("-topmost", True)
    overlay.wm_attributes("-transparentcolor", "white")
    canvas = tk.Canvas(overlay, width=20, height=20, bg="white", highlightthickness=0)
    canvas.pack()
    canvas.create_oval(2, 2, 18, 18, fill="red", outline="red")
    overlay.after(1000, overlay.destroy)
    overlay.mainloop()

print("📍 Getting current mouse position...")
x, y = pyautogui.position()
print(f"➡️ Moving mouse to (400, 400)")
pyautogui.moveTo(400, 400, duration=1.5)
print("✅ Showing overlay dot at (400, 400)")
create_overlay(400, 400)

print("✅ Overlay complete.")
