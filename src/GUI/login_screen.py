import tkinter as tk
from tkinter import messagebox
#from .entryScreen import entryScreen
from .createacc_screen import createAccountScreen
from repositories.player_repository import PlayerRepository

player_repo = PlayerRepository()

class Login_Class:
    def __init__(self):
        self.entry_username = None
        self.entry_password = None
        self.login_screen_window = None
        self.player_repo = None
    
    def Login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.player_repo = PlayerRepository()
        player_id = self.player_repo.Player_login_check(username, password)

        if player_id:
            messagebox.showinfo("Success!", f"Login successfull, Welcome {username}.")
            self.Open_entryScreen()
        else:
            messagebox.showerror("Error!", "Wrong Username or Password.")

    def Open_entryScreen(self):
        from .entry_screen import entryScreen # to prevent a cycle
        self.login_screen_window.destroy()
        entryScreen(self.player_repo)

    def Open_create_account_screen(self):
        self.login_screen_window.destroy()
        # from .createacc_screen import create_account_screen  # Dynamic import
        createAccountScreen()

    def Login_screen(self):
        self.login_screen_window = tk.Tk()
        self.login_screen_window.title("Login System")
        self.login_screen_window.geometry("1200x800")
        self.login_screen_window.configure(bg="#2e2e2e")

        # Fonts and colours
        label_font = ("Helvetica", 16, "bold")
        btn_font = ("Helvetica", 14, "bold")
        btn_bg = "#444444"
        btn_fg = "#DDDDDD"
        entry_bg = "#3E3E3E"
        entry_fg = "#FFFFFF"

        # Frame for full centring
        frame = tk.Frame(self.login_screen_window, bg="#2e2e2e")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Username
        tk.Label(
            frame, text="Username:", font=label_font, fg="white", bg="#2e2e2e"
        ).pack(pady=5)
        self.entry_username = tk.Entry(
            frame, font=label_font, bg=entry_bg, fg=entry_fg, relief="flat"
        )
        self.entry_username.pack(pady=5)

        # Password
        tk.Label(frame, text="Password:", font=label_font, fg="white", bg="#2e2e2e").pack(
            pady=5
        )
        self.entry_password = tk.Entry(
            frame, font=label_font, bg=entry_bg, fg=entry_fg, show="*", relief="flat"
        )
        self.entry_password.pack(pady=5)

        # Login-Button
        btn_login = tk.Button(
            frame,
            text="Login",
            font=btn_font,
            bg=btn_bg,
            fg=btn_fg,
            relief="flat",
            command=self.Login,
        )
        btn_login.pack(pady=10, ipadx=20, ipady=10)

        # Create account button
        btn_create_account = tk.Button(
            frame,
            text="Create Account",
            font=btn_font,
            bg=btn_bg,
            fg=btn_fg,
            relief="flat",
            command=self.Open_create_account_screen,
        )
        btn_create_account.pack(pady=10, ipadx=20, ipady=10)

        self.login_screen_window.mainloop()