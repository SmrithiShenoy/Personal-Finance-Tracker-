import customtkinter as ctk
from tkinter import messagebox
import threading
import mysql.connector
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Mysql@2025",
    "database": "FINANCE_TRACKER"
}
         
def open_user_login():
    login_window = ctk.CTkToplevel()
    login_window.title("User Login")
    login_window.geometry("400x300")
    login_window.minsize(360, 280)
    login_window.configure(fg_color="#0a0f1f")
    ctk.CTkLabel(login_window, text="User Login", font=("Courier New", 20, "bold"),
                 text_color="#00fff0").pack(pady=12)

    email_entry = ctk.CTkEntry(login_window, placeholder_text="Email ID")
    email_entry.pack(padx=20, pady=8, fill="x")

    password_entry = ctk.CTkEntry(login_window, placeholder_text="Password", show="*")
    password_entry.pack(padx=20, pady=8, fill="x")

    def verify_user():
        email = email_entry.get().strip()
        pw = password_entry.get().strip()
        if not email or not pw:
            messagebox.showwarning("Missing Info", "Please fill in both fields.")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT USERID, Name FROM USER WHERE EmailID=%s AND PWD=%s",
                (email, pw)
            )
            row = cursor.fetchone()
            conn.close()

            if row:
                USERID, user_name = row[0], row[1]
                login_window.destroy()
                open_user_dashboard(USERID, user_name)
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not connect:\n{e}")

    ctk.CTkButton(login_window, text="Login", command=verify_user,
                  corner_radius=20,
                  fg_color="#051622", hover_color="#03e9f4",
                  text_color="#00fff0").pack(pady=20)
    def open_user_register():
        reg = ctk.CTkToplevel()
        reg.title("Register New User")
        reg.geometry("480x520")
        reg.minsize(420, 480)
        reg.configure(fg_color="#0b1a24")

        fields = [
            ("User ID", "e.g. U021"),
            ("Email ID", "you@mail.com"),
            ("Name", "Full name"),
            ("Password", "password"),
            ("DOB (YYYY-MM-DD)", "1990-01-01")
        ]
        entries = {}
        for label, ph in fields:
            ctk.CTkLabel(reg, text=label, text_color="#00fff0").pack(pady=(8, 4))
            ent = ctk.CTkEntry(reg, placeholder_text=ph, fg_color="#051622", text_color="#00fff0")
            ent.pack(padx=20, fill="x")
            entries[label] = ent

        # allow multiple phone numbers
        phone_entries = []
        ctk.CTkLabel(reg, text="Phone", text_color="#00fff0").pack(pady=(10, 4))
        phone_container = ctk.CTkFrame(reg, fg_color="transparent")
        phone_container.pack(padx=20, fill="x")

        def add_phone_field():
            p_ent = ctk.CTkEntry(phone_container, fg_color="#051622", text_color="#00fff0")
            p_ent.pack(pady=4, fill="x")
            phone_entries.append(p_ent)

        # initial phone field
        add_phone_field()
        ctk.CTkButton(reg, text="Add Phone", command=add_phone_field,
                      fg_color="#051622", hover_color="#03e9f4", text_color="#00fff0").pack(pady=(6, 8))

        ctk.CTkLabel(reg, text="Initial Account", text_color="#00fff0").pack(pady=(12, 4))
        acct_fields = ["Account ID", "Account Name", "Type", "Current Balance"]
        acct_entries = {}
        for af in acct_fields:
            ctk.CTkLabel(reg, text=af, text_color="#00fff0").pack(pady=(6, 2))
            aent = ctk.CTkEntry(reg, fg_color="#051622", text_color="#00fff0")
            aent.pack(padx=20, fill="x")
            acct_entries[af] = aent

        def create_user():
            uid = entries["User ID"].get().strip()
            email = entries["Email ID"].get().strip()
            name = entries["Name"].get().strip()
            pwd = entries["Password"].get().strip()
            dob = entries["DOB (YYYY-MM-DD)"].get().strip() or None
            # collect phone numbers from the phone entry list
            phone = None
            phones_list = []
            try:
                for p_ent in phone_entries:
                    val = p_ent.get().strip()
                    if val:
                        phones_list.append(val)
            except Exception:
                pass
            if phones_list:
                phone = phones_list

            acc_id = acct_entries["Account ID"].get().strip()
            acc_name = acct_entries["Account Name"].get().strip()
            acc_type = acct_entries["Type"].get().strip()
            acc_bal = acct_entries["Current Balance"].get().strip() or None

            if not uid or not email or not name or not pwd:
                messagebox.showwarning("Missing", "User ID, Email, Name and Password are required.")
                return

            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute("INSERT INTO `USER` (USERID, EmailID, Name, PWD, DOB) VALUES (%s,%s,%s,%s,%s)",
                            (uid, email, name, pwd, dob))
                if phones_list:
                    for ph in phones_list:
                        try:
                            cur.execute("INSERT INTO Phone (USERID, Phone) VALUES (%s,%s)", (uid, ph))
                        except Exception:
                            # ignore individual phone insert errors
                            pass
                if acc_id and acc_name:
                    try:
                        cur.execute("INSERT INTO Accounts (ACCID, USERID, AccNa, Type, Curren_Bal) VALUES (%s,%s,%s,%s,%s)",
                                    (acc_id, uid, acc_name, acc_type or None, acc_bal or 0))
                    except Exception:
                        # if account insert fails, continue but report later
                        pass

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User registered successfully. You can now log in.")
                reg.destroy()
            except mysql.connector.IntegrityError as ie:
                messagebox.showerror("Error", f"Integrity error: {ie}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create user:\n{e}")

        ctk.CTkButton(reg, text="Create User", command=create_user, fg_color="#00fff0", text_color="#000", corner_radius=20).pack(pady=16)

    ctk.CTkButton(login_window, text="Register", command=open_user_register,
                  corner_radius=20,
                  fg_color="#051622", hover_color="#03e9f4",
                  text_color="#00fff0").pack()



def display_table(df: pd.DataFrame, parent):
    """
    Clear `parent` and render dataframe in a scrollable area with equally spaced columns.
    """
    for w in parent.winfo_children():
        w.destroy()

    scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="#091a20")
    scroll_frame.pack(pady=10, fill="both", expand=True)

    if df is None or df.empty:
        ctk.CTkLabel(scroll_frame, text="No records found.", text_color="#00fff0",
                     font=("Courier New", 14)).pack(pady=20)
        return

    num_cols = len(df.columns)
    for j in range(num_cols):
        scroll_frame.grid_columnconfigure(j, weight=1, uniform="col")

    for j, col in enumerate(df.columns):
        ctk.CTkLabel(scroll_frame, text=str(col), anchor="w",
                     font=("Courier New", 13, "bold"), text_color="#00fff0").grid(row=0, column=j, padx=6, pady=6, sticky="ew")

    for i, row in enumerate(df.itertuples(index=False), start=1):
        for j, val in enumerate(row):
            ctk.CTkLabel(scroll_frame, text=str(val), anchor="w",
                         text_color="#00fff0", font=("Courier New", 12)).grid(row=i, column=j, padx=6, pady=4, sticky="ew")


def build_accounts_section(parent, USERID):
    """Create Accounts UI inside parent. CRUD operations refresh the content area."""
    title = ctk.CTkLabel(parent, text="🏦 Your Accounts", text_color="#03e9f4",
                         font=("Courier New", 18, "bold"))
    title.pack(pady=10)

    content_frame = ctk.CTkFrame(parent, fg_color="#0b1a24")
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(pady=8)

    def fetch_accounts():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            df = pd.read_sql(f"SELECT ACCID, AccNa, Type, Curren_Bal FROM Accounts WHERE USERID=%s",
                             conn, params=(USERID,))
            conn.close()
            display_table(df, content_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch accounts:\n{e}")

    def add_account():
        add_win = ctk.CTkToplevel()
        add_win.title("Add Account")
        add_win.geometry("420x350")
        add_win.minsize(380, 300)
        add_win.configure(fg_color="#0b1a24")

        labels = ["Account ID", "Name", "Type", "Current Balance"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=(8, 4))
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0")
            ent.pack(padx=20, fill="x")
            entries[lbl] = ent

        def save_account():
            accid = entries["Account ID"].get().strip()
            name = entries["Name"].get().strip()
            typ = entries["Type"].get().strip()
            bal = entries["Current Balance"].get().strip() or "0"
            if not accid or not name:
                messagebox.showwarning("Missing", "Account ID and Name are required.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Accounts (ACCID, USERID, AccNa, Type, Curren_Bal) VALUES (%s, %s, %s, %s, %s)",
                    (accid, USERID, name, typ, bal)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Account added successfully!")
                add_win.destroy()
                fetch_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Could not add account:\n{e}")

        ctk.CTkButton(add_win, text="Save", command=save_account,
                      fg_color="#00fff0", text_color="#000", corner_radius=20).pack(pady=18)

    def update_balance():
        update_win = ctk.CTkToplevel()
        update_win.title("Update Balance")
        update_win.geometry("400x260")
        update_win.minsize(360, 220)
        update_win.configure(fg_color="#0b1a24")

        ctk.CTkLabel(update_win, text="Account ID", text_color="#00fff0").pack(pady=6)
        a_ent = ctk.CTkEntry(update_win, fg_color="#051622", text_color="#00fff0")
        a_ent.pack(padx=20, fill="x")
        ctk.CTkLabel(update_win, text="New Balance", text_color="#00fff0").pack(pady=6)
        b_ent = ctk.CTkEntry(update_win, fg_color="#051622", text_color="#00fff0")
        b_ent.pack(padx=20, fill="x")

        def save_update():
            accid = a_ent.get().strip()
            bal = b_ent.get().strip()
            if not accid or bal == "":
                messagebox.showwarning("Missing", "Please provide Account ID and new balance.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute("UPDATE Accounts SET Curren_Bal=%s WHERE ACCID=%s", (bal, accid))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Balance updated!")
                update_win.destroy()
                fetch_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update balance:\n{e}")

        ctk.CTkButton(update_win, text="Update", command=save_update,
                      fg_color="#00fff0", text_color="#000", corner_radius=20).pack(pady=14)

    def delete_account():
        accid = ctk.CTkInputDialog(text="Enter Account ID to delete:", title="Delete Account").get_input()
        if not accid:
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("DELETE FROM Accounts WHERE ACCID=%s", (accid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Account deleted successfully!")
            fetch_accounts()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete account:\n{e}")

    ctk.CTkButton(btn_frame, text="Add Account", command=add_account,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=140).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Update Balance", command=update_balance,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=140).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Delete Account", command=delete_account,
                  fg_color="#051622", text_color="#ff4444", corner_radius=20, width=140).pack(side="left", padx=8)

    fetch_accounts()


def build_transactions_section(parent, USERID):
    title = ctk.CTkLabel(parent, text="💸 Your Transactions", text_color="#00fff0",
                         font=("Courier New", 18, "bold"))
    title.pack(pady=10)

    content_frame = ctk.CTkFrame(parent, fg_color="#0b1a24")
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(pady=8)

    def fetch_transactions():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            query = """
                SELECT T.TXID, T.ACCID, T.CID, T.expense, T.mode, T.time
                FROM `Transaction` T
                JOIN Accounts A ON T.ACCID = A.ACCID
                WHERE A.USERID = %s
                ORDER BY T.time DESC
            """
            df = pd.read_sql(query, conn, params=(USERID,))
            conn.close()
            display_table(df, content_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch transactions:\n{e}")

    def add_transaction():
        add_win = ctk.CTkToplevel()
        add_win.title("Add Transaction")
        add_win.geometry("420x420")
        add_win.minsize(380, 380)
        add_win.configure(fg_color="#0b1a24")

        labels = ["Transaction ID", "Account ID", "Category ID", "Expense Amount", "Mode (cash/card)", "Time (YYYY-MM-DD HH:MM:SS)"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=(8, 4))
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0")
            ent.pack(padx=20, fill="x")
            entries[lbl] = ent

        def save_transaction():
            vals = [entries[l].get().strip() for l in labels]
            if not vals[0] or not vals[1] or not vals[3]:
                messagebox.showwarning("Missing", "TXID, Account ID and Expense are required.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()

                cur.execute("SELECT GetAccountBalance(%s)", (vals[1],))
                old_bal = cur.fetchone()[0]
                messagebox.showinfo("Before Transaction", f"Current Balance: ₹{old_bal:.2f}")

                cur.execute("""
                    INSERT INTO `Transaction` (TXID, ACCID, CID, expense, mode, time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, tuple(vals))

                conn.commit()

                cur.execute("SELECT GetAccountBalance(%s)", (vals[1],))
                new_bal = cur.fetchone()[0]

                messagebox.showinfo("After Transaction", f"Updated Balance: ₹{new_bal:.2f}")

                conn.close()
                messagebox.showinfo("Success", "Transaction added successfully!\n(Trigger executed!)")
                add_win.destroy()
                fetch_transactions()

            except Exception as e:
                messagebox.showerror("Error", f"Could not add transaction:\n{e}")


        ctk.CTkButton(add_win, text="Save", command=save_transaction,
                      fg_color="#00fff0", text_color="#000", corner_radius=20).pack(pady=18)

    def delete_transaction():
        txid = ctk.CTkInputDialog(text="Enter Transaction ID to delete:", title="Delete Transaction").get_input()
        if not txid:
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("DELETE FROM `Transaction` WHERE TXID=%s", (txid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Transaction deleted successfully!")
            fetch_transactions()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete transaction:\n{e}")

    ctk.CTkButton(btn_frame, text="Add Transaction", command=add_transaction,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=160).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Delete Transaction", command=delete_transaction,
                  fg_color="#051622", text_color="#ff4444", corner_radius=20, width=160).pack(side="left", padx=8)

    fetch_transactions()

    


def build_goals_section(parent, USERID):
    title = ctk.CTkLabel(parent, text="🎯 Your Goals", text_color="#03e9f4",
                         font=("Courier New", 18, "bold"))
    title.pack(pady=10)

    content_frame = ctk.CTkFrame(parent, fg_color="#0b1a24")
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(pady=8)

    def fetch_goals():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            df = pd.read_sql("SELECT GID, title, Target, deadline FROM Goals WHERE USERID=%s", conn, params=(USERID,))
            conn.close()
            display_table(df, content_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch goals:\n{e}")

    def add_goal():
        add_win = ctk.CTkToplevel()
        add_win.title("Add Goal")
        add_win.geometry("420x380")
        add_win.minsize(380, 340)
        add_win.configure(fg_color="#0b1a24")

        labels = ["Goal ID", "Title", "Target Amount", "Deadline (YYYY-MM-DD)"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=(8, 4))
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0")
            ent.pack(padx=20, fill="x")
            entries[lbl] = ent

        def save_goal():
            gid = entries["Goal ID"].get().strip()
            title = entries["Title"].get().strip()
            target = entries["Target Amount"].get().strip()
            deadline = entries["Deadline (YYYY-MM-DD)"].get().strip()
            if not gid or not title:
                messagebox.showwarning("Missing", "Goal ID and Title required.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute("INSERT INTO Goals (GID, USERID, title, Target, deadline) VALUES (%s, %s, %s, %s, %s)",
                            (gid, USERID, title, target, deadline))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Goal added successfully!")
                add_win.destroy()
                fetch_goals()
            except Exception as e:
                messagebox.showerror("Error", f"Could not add goal:\n{e}")

        ctk.CTkButton(add_win, text="Save", command=save_goal,
                      fg_color="#00fff0", text_color="#000", corner_radius=20).pack(pady=14)

    def delete_goal():
        gid = ctk.CTkInputDialog(text="Enter Goal ID to delete:", title="Delete Goal").get_input()
        if not gid:
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("DELETE FROM Goals WHERE GID=%s", (gid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Goal deleted successfully!")
            fetch_goals()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete goal:\n{e}")

    ctk.CTkButton(btn_frame, text="Add Goal", command=add_goal,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=140).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Delete Goal", command=delete_goal,
                  fg_color="#051622", text_color="#ff4444", corner_radius=20, width=140).pack(side="left", padx=8)

    fetch_goals()


def build_budget_section(parent, USERID):
    title = ctk.CTkLabel(parent, text="💰 Your Budgets", text_color="#03e9f4",
                         font=("Courier New", 18, "bold"))
    title.pack(pady=10)

    content_frame = ctk.CTkFrame(parent, fg_color="#0b1a24")
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(pady=8)

    def fetch_budget():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            df = pd.read_sql("SELECT BID, CID, Month, Year, Limit_Amt FROM Budget WHERE USERID=%s", conn, params=(USERID,))
            conn.close()
            display_table(df, content_frame)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch budgets:\n{e}")

    def add_budget():
        add_win = ctk.CTkToplevel()
        add_win.title("Add Budget")
        add_win.geometry("420x360")
        add_win.configure(fg_color="#0b1a24")

        labels = ["Budget ID", "Category ID", "Month", "Year", "Limit Amount"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=6)
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0", width=300)
            ent.pack()
            entries[lbl] = ent

        def save_budget():
            bid = entries["Budget ID"].get().strip()
            cid = entries["Category ID"].get().strip()
            month = entries["Month"].get().strip()
            year = entries["Year"].get().strip()
            limit = entries["Limit Amount"].get().strip()
            if not bid or not cid:
                messagebox.showwarning("Missing", "Budget ID and Category ID required.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()
                cur.execute("INSERT INTO Budget (BID, USERID, CID, Month, Year, Limit_Amt) VALUES (%s, %s, %s, %s, %s, %s)",
                            (bid, USERID, cid, month, year, limit))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Budget added successfully!")
                add_win.destroy()
                fetch_budget()
            except Exception as e:
                messagebox.showerror("Error", f"Could not add budget:\n{e}")

        ctk.CTkButton(add_win, text="Save", command=save_budget,
                      fg_color="#00fff0", text_color="#000", corner_radius=20).pack(pady=14)

    def delete_budget():
        bid = ctk.CTkInputDialog(text="Enter Budget ID to delete:", title="Delete Budget").get_input()
        if not bid:
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("DELETE FROM Budget WHERE BID=%s", (bid,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Budget deleted successfully!")
            fetch_budget()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete budget:\n{e}")

    ctk.CTkButton(btn_frame, text="Add Budget", command=add_budget,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=140).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Delete Budget", command=delete_budget,
                  fg_color="#051622", text_color="#ff4444", corner_radius=20, width=140).pack(side="left", padx=8)

    fetch_budget()


def build_reports_section(parent, USERID):
    """Create a small reports UI where users can run three report/query types.
    Uses background threads and `display_table` to show results.
    """
    title = ctk.CTkLabel(parent, text="📊 Reports & Queries", text_color="#03e9f4",
                         font=("Courier New", 18, "bold"))
    title.pack(pady=10)

    content_frame = ctk.CTkFrame(parent, fg_color="#0b1a24")
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(pady=8)


    controls_to_toggle = []

    status_var = {"label": None}
    def set_status(text):
        lbl = status_var.get("label")
        if lbl:
            lbl.configure(text=text)

    def set_controls_enabled(enabled: bool):
        for w in controls_to_toggle:
            try:
                w.configure(state=("normal" if enabled else "disabled"))
            except Exception:
                try:
                    w.configure(enabled=enabled)
                except Exception:
                    pass

    report_header = {"widget": None}

    def run_threaded_query(target, args=(), title=None):
        """Run target(*args) in a thread and catch exceptions to show in UI.
        Optionally show a report title above results for clarity.
        """
        set_status("Running...")
        set_controls_enabled(False)

        def runner():
            try:
                df = target(*args)

                def ui_update():
                    if report_header.get("widget"):
                        try:
                            report_header["widget"].destroy()
                        except Exception:
                            pass
                    if title:
                        report_header["widget"] = ctk.CTkLabel(parent, text=title, text_color="#00fff0", font=("Courier New", 12, "bold"))
                        report_header["widget"].pack(pady=(6, 0))
                    display_table(df, content_frame)
                    set_status(f"Done — {len(df)} rows")
                    set_controls_enabled(True)

                parent.after(0, ui_update)
            except Exception as e:
                parent.after(0, lambda: (messagebox.showerror("Query Error", str(e)), set_status("Error"), set_controls_enabled(True)))

        threading.Thread(target=runner, daemon=True).start()






    def fetch_groceries_transactions():
        """Run the example JOIN from your SQL file: list Groceries transactions with Account and User."""
        conn = mysql.connector.connect(**DB_CONFIG)
        sql = (
            "SELECT U.Name AS User_Name, A.AccNa AS Account_Name, T.expense AS Expense_Amount, T.time AS Transaction_Date "
            "FROM `Transaction` T "
            "JOIN Accounts A ON T.ACCID = A.ACCID "
            "JOIN `USER` U ON A.USERID = U.USERID "
            "JOIN Category C ON T.CID = C.CID "
            "WHERE C.C_Name = 'Groceries' AND A.USERID = %s "
            "ORDER BY T.time DESC"
        )
        df = pd.read_sql(sql, conn, params=(USERID,))
        conn.close()
        return df


    def fetch_oct_2024_by_category():
        """Return total spent per category for October 2024 (only positive expenses)."""
        conn = mysql.connector.connect(**DB_CONFIG)
        sql = (
            "SELECT C.C_Name AS Category_Name, SUM(T.expense) AS Total_Spent_Oct "
            "FROM `Transaction` T "
            "JOIN Category C ON T.CID = C.CID "
            "WHERE T.expense > 0 AND MONTH(T.time) = 10 AND YEAR(T.time) = 2024 "
            "GROUP BY C.C_Name "
            "ORDER BY Total_Spent_Oct DESC"
        )
        df = pd.read_sql(sql, conn)
        conn.close()
        return df


    btn_groceries = ctk.CTkButton(btn_frame, text="Groceries Txns", command=lambda: run_threaded_query(fetch_groceries_transactions, title="Groceries Transactions (Account, User, Amount, Time)"),
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=180)
    btn_groceries.pack(side="left", padx=8)
    btn3 = ctk.CTkButton(btn_frame, text="Monthly Spend (Oct 2024)", command=lambda: run_threaded_query(fetch_oct_2024_by_category, title="Total Spent by Category — Oct 2024"),
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=200)
    btn3.pack(side="left", padx=8)
    controls_to_toggle.extend([btn_groceries, btn3])

    status_lbl = ctk.CTkLabel(parent, text="Ready", text_color="#00fff0")
    status_lbl.pack(pady=(4, 0))
    status_var["label"] = status_lbl

    ctk.CTkLabel(content_frame, text="Run a report to see results here.", text_color="#00fff0").pack(pady=18)


def open_user_dashboard(USERID, user_name):
    win = ctk.CTkToplevel()
    win.title(f"Finance Tracker - {user_name}")
    win.geometry("1000x600")
    win.configure(fg_color="#0b1a24")

    sidebar = ctk.CTkFrame(win, width=200, fg_color="#051622", corner_radius=0)
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text=f"👤 {user_name}", text_color="#00fff0",
                 font=("Courier New", 16, "bold")).pack(pady=20)

    main_frame = ctk.CTkFrame(win, fg_color="#0b1a24")
    main_frame.pack(side="right", expand=True, fill="both", padx=8, pady=8)

    def clear_main():
        for w in main_frame.winfo_children():
            w.destroy()

    def open_accounts():
        clear_main()
        build_accounts_section(main_frame, USERID)

    def open_transactions():
        clear_main()
        build_transactions_section(main_frame, USERID)

    def open_goals():
        clear_main()
        build_goals_section(main_frame, USERID)

    def open_budgets():
        clear_main()
        build_budget_section(main_frame, USERID)

    def open_reports():
        clear_main()
        build_reports_section(main_frame, USERID)

    btns = [
        ("🏦 Accounts", open_accounts),
        ("💸 Transactions", open_transactions),
        ("🎯 Goals", open_goals),
        ("📈 Budgets", open_budgets),
        ("📊 Reports", open_reports),
        ("🚪 Logout", win.destroy),
    ]
    for text, cmd in btns:
        ctk.CTkButton(sidebar, text=text, command=cmd, width=170, fg_color="#051622",
                      text_color="#00fff0", hover_color="#03e9f4", corner_radius=15,
                      font=("Courier New", 13, "bold")).pack(pady=8)

    build_accounts_section(main_frame, USERID)
