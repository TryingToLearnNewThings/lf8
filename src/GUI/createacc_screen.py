import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from login_screen import login_screen


def create_account_screen():
    def create_account():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden.")
            return

        if password != confirm_password:
            messagebox.showerror("Fehler", "Passwörter stimmen nicht überein.")
            return

        # Datenbankverbindung für die Erstellung eines neuen Accounts
        con = sqlite3.connect("./Database/database.db")
        cursor = con.cursor()

        cursor.execute("SELECT * FROM Player WHERE Playername = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Fehler", "Benutzername ist bereits vergeben.")
            con.close()
            return

        cursor.execute(
            "INSERT INTO Player (Playername, playerPassword) VALUES (?, ?)",
            (username, password),
        )
        con.commit()
        con.close()

        messagebox.showinfo("Erfolg", "Account erfolgreich erstellt!")
        createacc_window.destroy()
        login_screen()

    createacc_window = tk.Tk()
    createacc_window.title("Account erstellen")
    createacc_window.geometry("1200x800")
    createacc_window.configure(bg="#2e2e2e")  # Standard-Hintergrundfarbe

    # Schriftarten und Farben
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"  # Dunkleres Grau für Buttons
    btn_fg = "#DDDDDD"  # Hellgrauer Text
    entry_bg = "#3E3E3E"  # Dunkles Grau für Eingabefelder
    entry_fg = "#FFFFFF"  # Weißer Text

    # Frame zum vollständigen Zentrieren
    frame = tk.Frame(createacc_window, bg="#2e2e2e")
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

    # Passwort bestätigen
    tk.Label(
        frame, text="Passwort bestätigen:", font=label_font, fg="white", bg="#2e2e2e"
    ).pack(pady=5)
    entry_confirm_password = tk.Entry(
        frame, font=label_font, bg=entry_bg, fg=entry_fg, show="*", relief="flat"
    )
    entry_confirm_password.pack(pady=5)

    # Account erstellen Button
    btn_create = tk.Button(
        frame,
        text="Account erstellen",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=create_account,
    )
    btn_create.pack(pady=10, ipadx=20, ipady=10)

    createacc_window.mainloop()
