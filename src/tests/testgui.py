import tkinter as tk


# Function to handle button click (you can modify the actions as needed)
def choose_mode(mode):
    print(f"Selected Mode: {mode}")
    # Here, you can proceed with the next screen or action based on the mode


# Main window
def choose_mode_window():
    window = tk.Tk()
    window.title("Choose Your Mode")
    window.geometry("600x400")
    window.configure(bg="#1e1e1e")

    # Styling
    label_font = ("Arial", 16, "bold")
    btn_font = ("Arial", 80, "bold")  # Emojis bleiben groß
    btn_bg = "#00BFFF"
    btn_fg = "black"
    description_font = ("Arial", 12, "normal")

    # Title Label
    title_label = tk.Label(
        window, text="Choose Your Mode", font=label_font, fg="white", bg="#1e1e1e"
    )
    title_label.pack(pady=20)

    # Frame to hold both buttons and descriptions (center the content)
    frame = tk.Frame(window, bg="#1e1e1e")
    frame.pack(expand=True)  # Allow the frame to expand and center its content

    # Simulating shadow effect using a slightly offset second button (first button shadow)
    shadow_offset = 5  

    # Single Player Button with Shadow
    single_player_shadow = tk.Button(
        frame,
        text="🧑‍💻",
        font=btn_font,
        bg="#0080FF",
        fg=btn_fg,
        width=4,
        height=2,
        relief="solid",
        bd=2,
    )
    single_player_shadow.grid(row=0, column=0, padx=shadow_offset, pady=shadow_offset)

    # Single Player Button (Main button)
    single_player_btn = tk.Button(
        frame,
        text="🧑‍💻",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        width=4,
        height=2,
        relief="solid",
        bd=2,
        borderwidth=4,
        highlightthickness=0,
    )
    single_player_btn.grid(row=0, column=0, padx=10, pady=10)

    single_player_desc = tk.Label(
        frame, text="Singleplayer", font=description_font, fg="white", bg="#1e1e1e"
    )
    single_player_desc.grid(row=1, column=0)

    # Multiplayer Button with Shadow
    multiplayer_shadow = tk.Button(
        frame,
        text="👾",
        font=btn_font,
        bg="#0080FF",
        fg=btn_fg,
        width=4,
        height=2,
        relief="solid",
        bd=2,
    )
    multiplayer_shadow.grid(row=0, column=1, padx=shadow_offset, pady=shadow_offset)

    # Multiplayer Button (Main button)
    multiplayer_btn = tk.Button(
        frame,
        text="👾",
        font=btn_font,
        bg=btn_bg,
        fg=btn_fg,
        width=4,
        height=2,
        relief="solid",
        bd=2,
        borderwidth=4,
        highlightthickness=0,
    )
    multiplayer_btn.grid(row=0, column=1, padx=10, pady=10)

    multiplayer_desc = tk.Label(
        frame, text="Multiplayer", font=description_font, fg="white", bg="#1e1e1e"
    )
    multiplayer_desc.grid(row=1, column=1)

    window.mainloop()



choose_mode_window()
