import threading
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Mysql@2025",
    "database": "FINANCE_TRACKER"
}

def get_tables():
    """Return list of all table names in the database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        messagebox.showerror("Database Error", f"Unable to fetch tables:\n{e}")
        return []

def open_admin_login(parent=None):
    """Popup admin login. Call open_admin_dashboard() on success."""
    login_window = ctk.CTkToplevel(master=parent) if parent else ctk.CTkToplevel()
    login_window.title("Admin Login")
    login_window.geometry("400x250")
    login_window.configure(fg_color="#0f2027")

    title = ctk.CTkLabel(
        login_window,
        text="🔐 Admin Login",
        font=("Courier New", 20, "bold"),
        text_color="#00fff0"
    )
    title.pack(pady=20)

    pw_label = ctk.CTkLabel(
        login_window,
        text="Enter Password:",
        font=("Courier New", 14),
    text_color="#00fff0"
    )
    pw_label.pack(pady=10)

    pw_entry = ctk.CTkEntry(
        login_window,
        show="*",
        width=220,
        fg_color="#051622",
        text_color="#00fff0",
        border_color="#00fff0",
        corner_radius=10
    )
    pw_entry.pack(pady=5)

    def verify_password():
        if pw_entry.get() == "admin123":
            login_window.destroy()
            open_admin_dashboard("ADMIN001", " ")
        else:
            messagebox.showerror("Access Denied", "Incorrect password. Try again!")

    ctk.CTkButton(
        login_window,
        text="Login",
        fg_color="#051622",
        hover_color="#03e9f4",
        text_color="#00fff0",
        font=("Courier New", 14, "bold"),
        corner_radius=25,
        width=120,
        height=40,
        border_width=2,
        border_color="#00fff0",
        command=verify_password
    ).pack(pady=25)

def open_admin_dashboard(userid, name):
    app = ctk.CTkToplevel()
    app.title("Admin Dashboard")
    app.geometry("1000x600")
    app.configure(fg_color="#0b1a24")

    ctk.CTkLabel(
        app,
        text=f"Welcome Admin {name}",
        font=("Courier New", 22, "bold"),
        text_color="#00fff0"
    ).pack(pady=20)

    top_frame = ctk.CTkFrame(app, fg_color="#102a3a", corner_radius=15)
    top_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(top_frame, text="Select Table:", text_color="#00fff0", font=("Courier New", 14)).pack(side="left", padx=10)

    tables = get_tables()
    if not tables:
        messagebox.showerror("Error", "No tables found in the database.")
        return

    table_var = ctk.StringVar(value=tables[0])

    table_frame = ctk.CTkScrollableFrame(app, fg_color="#102a3a", corner_radius=15, width=900, height=400)
    table_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def show_table_data(table_name):
        """Fetch and display table data dynamically"""
        for widget in table_frame.winfo_children():
            widget.destroy()  # Clear old content

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        num_cols = len(columns)
        for j in range(num_cols):
            table_frame.grid_columnconfigure(j, weight=1, uniform="col")

        for j, col in enumerate(columns):
            header = ctk.CTkLabel(
                table_frame,
                text=col,
                font=("Courier New", 13, "bold"),
                text_color="#00fff0",
                anchor="w"
            )
            header.grid(row=0, column=j, padx=10, pady=5, sticky="ew")

        for i, row in enumerate(rows, start=1):
            for j, val in enumerate(row):
                cell = ctk.CTkLabel(
                    table_frame,
                    text=str(val),
                    font=("Courier New", 12),
                    text_color="#fff",
                    anchor="w"
                )
                cell.grid(row=i, column=j, padx=10, pady=3, sticky="ew")

    dropdown = ctk.CTkOptionMenu(
        top_frame,
        variable=table_var,
        values=tables,
        fg_color="#00fff0",
        text_color="#000",
        command=lambda _: threading.Thread(
            target=show_table_data, args=(table_var.get(),), daemon=True
        ).start()
    )
    dropdown.pack(side="left", padx=10, pady=10)

    def run_users_budget_above_avg_admin():
        def worker():
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                sql = (
                    "SELECT U.Name FROM `USER` AS U "
                    "JOIN Budget AS B ON U.USERID = B.USERID "
                    "WHERE B.Limit_Amt > (SELECT AVG(Limit_Amt) FROM Budget) "
                    "GROUP BY U.Name"
                )
                cur.execute(sql)
                rows = cur.fetchall()
                cols = [desc[0] for desc in cur.description]
                conn.close()

                def ui_update():
                    for widget in table_frame.winfo_children():
                        widget.destroy()

                    num_cols = len(cols)
                    for j in range(num_cols):
                        table_frame.grid_columnconfigure(j, weight=1, uniform="col")

                    for j, col in enumerate(cols):
                        header = ctk.CTkLabel(table_frame, text=col, font=("Courier New", 13, "bold"), text_color="#00fff0", anchor="w")
                        header.grid(row=0, column=j, padx=10, pady=5, sticky="ew")

                    for i, row in enumerate(rows, start=1):
                        for j, val in enumerate(row):
                            cell = ctk.CTkLabel(table_frame, text=str(val), font=("Courier New", 12), text_color="#fff", anchor="w")
                            cell.grid(row=i, column=j, padx=10, pady=3, sticky="ew")

                app.after(0, ui_update)
            except Exception as e:
                app.after(0, lambda: messagebox.showerror("Query Error", str(e)))

        threading.Thread(target=worker, daemon=True).start()

    ctk.CTkButton(top_frame, text="Users > Budget > Above Avg", fg_color="#051622", text_color="#00fff0",
                  corner_radius=12, command=run_users_budget_above_avg_admin).pack(side="left", padx=8)

    threading.Thread(target=show_table_data, args=(tables[0],), daemon=True).start()

    app.mainloop()
