import tkinter as tk
from tkinter import ttk, messagebox
from repositories.player_repository import PlayerRepository
import sqlite3
# from GUI.login_screen import Login
player_repo = PlayerRepository()

def createAccountScreen():
    
    def createAccount():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All Inputs need to be filled")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        player_name_taken =player_repo.Get_value_from_table("Player","*","playerName", username)
        
        # Database connection for the creation of a new account
        # con = sqlite3.connect("./Database/database.db")
        # cursor = con.cursor()

        # cursor.execute("SELECT * FROM Player WHERE Playername = ?", (username,))
        if player_name_taken:
            messagebox.showerror("Error", "Username is already taken")
            return

        player_repo.create_user(username,password)

        messagebox.showinfo("Success", "Account created successfully")
        createacc_window.destroy()



    createacc_window = tk.Tk()
    createacc_window.title("Create Account")
    createacc_window.geometry("1200x800")
    createacc_window.configure(bg="#2e2e2e")

    # Fonts and colours
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"
    btn_fg = "#DDDDDD"
    entry_bg = "#3E3E3E"
    entry_fg = "#FFFFFF"

    # Frame for complete centring
    frame = tk.Frame(createacc_window, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Username
    tk.Label(
        frame, text="Username:", font=label_font, fg="white", bg="#2e2e2e"
    ).pack(pady=5)
    entry_username = tk.Entry(
        frame, font=label_font, bg=entry_bg, fg=entry_fg, relief="flat"
    )
    entry_username.pack(pady=5)

    # Password
    tk.Label(frame, text="Password:", font=label_font, fg="white", bg="#2e2e2e").pack(
        pady=5
    )
    entry_password = tk.Entry(
        frame, font=label_font, bg=entry_bg, fg=entry_fg, show="*", relief="flat"
    )
    entry_password.pack(pady=5)

    # Confirm password
    tk.Label(
        frame, text="Confirm Password:", font=label_font, fg="white", bg="#2e2e2e"
    ).pack(pady=5)
    entry_confirm_password = tk.Entry(
        frame, font=label_font, bg=entry_bg, fg=entry_fg, show="*", relief="flat"
    )
    entry_confirm_password.pack(pady=5)

    # Create account button
    btn_create = tk.Button(
        frame,
        text="Create Account",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=createAccount,
    )
    btn_create.pack(pady=10, ipadx=20, ipady=10)

    createacc_window.mainloop()


