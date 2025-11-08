import customtkinter as ctk
import tkinter as tk
from admin_dashboard import open_admin_login
from user_dashboard import open_user_login
from colors import ACCENT, HOVER, BTN_BG, BTN_BORDER, BG, BG_ALT, TEXT_LIGHT

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Finance Tracker")
app.geometry("750x500")
app.minsize(650, 420)

app.configure(fg_color=BG)

frame = ctk.CTkFrame(master=app, fg_color="transparent")
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.grid_columnconfigure(0, weight=1)

title = ctk.CTkLabel(
    master=frame,
    text="Welcome to your very own personalised finance tracker!",
    font=("Courier New", 20, "bold"),
    text_color=ACCENT,
)
title.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 18))

who = ctk.CTkLabel(
    master=frame,
    text="Who are you?",
    font=("Courier New", 16),
    text_color=ACCENT,
)
who.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

def neon_button(master, text, command=None):
    return ctk.CTkButton(
        master=master,
        text=text,
        fg_color=BTN_BG,
        hover_color=HOVER,
        text_color=TEXT_LIGHT,
        font=("Courier New", 14, "bold"),
        corner_radius=25,
        height=45,
        border_width=2,
        border_color=BTN_BORDER,
        command=command,
    )

btn_row = ctk.CTkFrame(master=frame, fg_color="transparent")
btn_row.grid(row=2, column=0, pady=12, padx=6, sticky="ew")
btn_row.grid_columnconfigure(0, weight=1)
btn_row.grid_columnconfigure(1, weight=1)

admin_btn = neon_button(btn_row, "Admin", command=open_admin_login)
user_btn = neon_button(btn_row, "User", command=open_user_login)
admin_btn.grid(row=0, column=0, padx=(20, 10), sticky="e")
user_btn.grid(row=0, column=1, padx=(10, 20), sticky="w")

app.mainloop()
