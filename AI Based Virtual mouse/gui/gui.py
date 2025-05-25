import tkinter as tk

current_mode = "Initializing..."
mode_label = None

def update_mode(mode):
    global current_mode
    current_mode = mode
    if mode_label:
        mode_label.config(text=f"Current Mode: {current_mode}")

def start_gui():
    global mode_label
    root = tk.Tk()
    root.title("Virtual Mouse AI")
    root.geometry("300x100")
    root.configure(bg="black")

    mode_label = tk.Label(root, text="Current Mode: Initializing...", font=("Arial", 14), fg="lime", bg="black")
    mode_label.pack(pady=30)

    root.mainloop()