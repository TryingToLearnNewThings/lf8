import tkinter as tk
from tkinter import ttk, messagebox
from entry_screen import entry_screen
import sqlite3


# Login-Funktion
def login():
    username = entry_username.get()
    password = entry_password.get()

    # Datenbankverbindung für Login
    con = sqlite3.connect("./Database/database.db")
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM Player WHERE Playername = ? AND playerPassword = ?",
        (username, password),
    )
    user = cursor.fetchone()
    con.close()

    if user:
        messagebox.showinfo("Erfolg", f"Login erfolgreich! Willkommen, {username}.")
        open_entry_screen()
    else:
        messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort.")


# Funktion, um den Entry Screen zu öffnen
def open_entry_screen():
    login_screen_window.destroy()
    entry_screen()


# Login-GUI
def login_screen():
    global entry_username, entry_password, login_screen_window

    login_screen_window = tk.Tk()
    login_screen_window.title("Login System")
    login_screen_window.geometry("1200x800")
    login_screen_window.configure(bg="#2e2e2e")  # Standard-Hintergrundfarbe

    # Schriftarten und Farben
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"  # Dunkleres Grau für Buttons
    btn_fg = "#DDDDDD"  # Hellgrauer Text
    entry_bg = "#3E3E3E"  # Dunkles Grau für Eingabefelder
    entry_fg = "#FFFFFF"  # Weißer Text

    # Frame zum vollständigen Zentrieren
    frame = tk.Frame(login_screen_window, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Benutzername
    tk.Label(
        frame, text="Benutzername:", font=label_font, fg="white", bg="#2e2e2e"
    ).pack(pady=5)
    entry_username = tk.Entry(
        frame, font=label_font, bg=entry_bg, fg=entry_fg, relief="flat"
    )
    entry_username.pack(pady=5)

    # Passwort
    tk.Label(frame, text="Passwort:", font=label_font, fg="white", bg="#2e2e2e").pack(
        pady=5
    )
    entry_password = tk.Entry(
        frame, font=label_font, bg=entry_bg, fg=entry_fg, show="*", relief="flat"
    )
    entry_password.pack(pady=5)

    # Login-Button
    btn_login = tk.Button(
        frame,
        text="Login",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=login,
    )
    btn_login.pack(pady=10, ipadx=20, ipady=10)

    # Account erstellen Button
    def open_create_account_screen():
        login_screen_window.destroy()
        from createacc_screen import create_account_screen  # Dynamischer Import

        create_account_screen()

    btn_create_account = tk.Button(
        login_screen_window,
        text="Account erstellen",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=open_create_account_screen,
    )
    btn_create_account.place(relx=0.9, rely=0.95, anchor="se")

    login_screen_window.mainloop()


if __name__ == "__main__":
    login_screen()