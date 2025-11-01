import customtkinter as ctk
import tkinter as tk
from admin_dashboard import open_admin_login
from user_dashboard import open_user_login

# ---------------------------
# MAIN APP WINDOW
# ---------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Finance Tracker")
app.geometry("750x500")

# Create cyber-style gradient illusion background
canvas = tk.Canvas(app, width=750, height=500, highlightthickness=0)
canvas.pack(fill="both", expand=True)
for i in range(0, 500):
    r = int(15 + (30 - 15) * (i / 500))
    g = int(32 + (83 - 32) * (i / 500))
    b = int(39 + (100 - 39) * (i / 500))
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 750, i, fill=color)

frame = ctk.CTkFrame(master=app, fg_color="transparent")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Welcome text
title = ctk.CTkLabel(
    master=frame,
    text="Welcome to your very own personalised finance tracker!",
    font=("Courier New", 20, "bold"),
    text_color="#00fff0",
)
title.pack(pady=(20, 30))

who = ctk.CTkLabel(
    master=frame,
    text="Who are you?",
    font=("Courier New", 16),
    text_color="#00eaff",
)
who.pack(pady=10)

# Reusable neon button style
def neon_button(master, text, command=None):
    return ctk.CTkButton(
        master=master,
        text=text,
        fg_color="#051622",
        hover_color="#03e9f4",
        text_color="#00fff0",
        font=("Courier New", 14, "bold"),
        corner_radius=25,
        width=160,
        height=45,
        border_width=2,
        border_color="#00fff0",
        command=command,
    )

# Buttons for Admin / User
admin_btn = neon_button(frame, "Admin", command=open_admin_login)
user_btn = neon_button(frame, "User", command=open_user_login)
admin_btn.pack(side="left", padx=30, pady=20)
user_btn.pack(side="right", padx=30, pady=20)

app.mainloop()
