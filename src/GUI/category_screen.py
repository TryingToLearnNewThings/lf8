import sys
import os

# Adds the main folder to the Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from repositories.category_repository import CategoryRepository
from .gameplay_screen import GameplayScreen

category_repo = CategoryRepository()

# player can choos a categry
def categoryScreen(player_repo):
    root = tk.Tk()
    root.title("Choose your category")
    root.geometry("1200x800")
    root.configure(bg="#2e2e2e")

    # Fonts and colours
    label_font = ("Helvetica", 16, "bold")
    btn_font = ("Helvetica", 14, "bold")
    btn_bg = "#444444"  
    btn_fg = "#DDDDDD"

    # Frame for complete centring
    frame = tk.Frame(root, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Category selection Label
    tk.Label(
        frame,
        text="Choose a Category",
        font=label_font,
        fg="white",
        bg="#2e2e2e",
    ).pack(pady=20)

    # Buttons for categories
    categories = category_repo.Get_category_name()

    for category in categories:
        btn = tk.Button(
            frame,
            text=category,
            font=btn_font,
            bg=btn_bg,
            fg=btn_fg,
            relief="flat",
            command=lambda c=category: Start_gameplay(root, c, player_repo),
        )
        btn.pack(pady=15, ipadx=10, ipady=10)

    root.mainloop()


def Start_gameplay(root, selected_category, player_repo):
    """
    Startet den GameplayScreen basierend auf der ausgewählten Kategorie.
    """
    print(f"Ausgewählte Kategorie: {selected_category}")
    
    # Gets the category ID based on the name
    category_id = category_repo.Get_category_id_by_name(selected_category)
    print(f"Category ID: {category_id}")
    
    # Closes the category screen
    root.destroy()
    
    # Starts the gameplay screen with the category ID
    GameplayScreen(category_id=category_id, player_repo = player_repo)

