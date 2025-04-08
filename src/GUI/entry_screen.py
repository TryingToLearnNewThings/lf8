import tkinter as tk
from tkinter import ttk
from category_screen import category_screen
from achievement_screen import achievement_screen
from helper_screen import helper_screen


# Funktion, um die Kategorieauswahl zu öffnen
# Schließt Entry-screen und startet Kategorieauswahl-screen
def open_category_screen():
    main_screen.destroy()
    category_screen()


# Hauptbildschirm (Entry Screen)
def entry_screen():
    global main_screen
    main_screen = tk.Tk()
    main_screen.title("Hauptmenü")
    main_screen.geometry("1200x800")
    main_screen.configure(bg="#2e2e2e")  # Standard-Hintergrundfarbe

    # Schriftarten und Farben
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"  # Dunkleres Grau für Buttons
    btn_fg = "#DDDDDD"  # Hellgrauer Text

    # Frame zum vollständigen Zentrieren
    frame = tk.Frame(main_screen, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Titel-Label
    tk.Label(
        frame,
        text="Willkommen im Quiz-Spiel!",
        font=label_font,
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Button zur Kategorieauswahl
    tk.Button(
        frame,
        text="Kategorie auswählen",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=open_category_screen,
    ).pack(pady=10, ipadx=20, ipady=10)

    # Button zu den Achievements
    tk.Button(
        frame,
        text="Achievements anzeigen",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=open_achievement_screen,
    ).pack(pady=10, ipadx=20, ipady=10)

    # Button for the helper screen in the bottom-right corner
    help_button = tk.Button(
        main_screen,
        text="Hilfe",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        relief="flat",
        command=helper_screen,  # Open the helper screen
    )
    help_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)  # Bottom-right corner with padding

    # Bind the "h" key to open the helper screen
    main_screen.bind("h", lambda event: helper_screen())

    main_screen.mainloop()

# Schhließt Entry-screen und öffnet Achievement-screen
def open_achievement_screen():
    main_screen.destroy()
    achievement_screen()
