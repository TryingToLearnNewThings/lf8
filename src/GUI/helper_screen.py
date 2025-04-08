import tkinter as tk

def helper_screen():
    # Create the helper screen window
    helper_window = tk.Toplevel()
    helper_window.title("Hilfe")
    helper_window.geometry("800x600")
    helper_window.configure(bg="#2e2e2e")

    # Add a label with instructions or help text
    tk.Label(
        helper_window,
        text="Willkommen im Hilfebereich!\nHier finden Sie nützliche Informationen.",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2e2e2e",
        wraplength=700,
        justify="center",
    ).pack(pady=20)

    # Add a close button
    tk.Button(
        helper_window,
        text="Schließen",
        font=("Helvetica", 14, "bold"),
        bg="#444444",
        fg="#DDDDDD",
        relief="flat",
        command=helper_window.destroy,
    ).pack(pady=20, ipadx=20, ipady=10)