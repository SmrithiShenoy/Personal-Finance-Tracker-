import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import pandas as pd

# ---------------- DATABASE CONFIG ----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "mysql123",
    "database": "FINANCE_TRACKER"
}
         
# =================================================
#  USER LOGIN
# =================================================
def open_user_login():
    login_window = ctk.CTkToplevel()
    login_window.title("User Login")
    login_window.geometry("400x300")
    login_window.configure(fg_color="#0a0f1f")

    ctk.CTkLabel(login_window, text="User Login", font=("Courier New", 20, "bold"),
                 text_color="#00fff0").pack(pady=15)

    email_entry = ctk.CTkEntry(login_window, placeholder_text="Email ID", width=250)
    email_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(login_window, placeholder_text="Password", show="*", width=250)
    password_entry.pack(pady=10)

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
                  width=120, corner_radius=20,
                  fg_color="#051622", hover_color="#03e9f4",
                  text_color="#00fff0").pack(pady=20)



# -------------------- Table display utility --------------------
def display_table(df: pd.DataFrame, parent):
    """
    Clear `parent` and render dataframe in a scrollable area with equally spaced columns.
    """
    for w in parent.winfo_children():
        w.destroy()

    scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="#091a20", width=800, height=380)
    scroll_frame.pack(pady=10, fill="both", expand=True)

    # empty
    if df is None or df.empty:
        ctk.CTkLabel(scroll_frame, text="No records found.", text_color="#00fff0",
                     font=("Courier New", 14)).pack(pady=20)
        return

    # compute equal width (approx) — allow a minimum width
    num_cols = len(df.columns)
    total_width = max(700, 120 * num_cols)  # widen if many cols
    col_width = int(total_width / num_cols)

    # header row
    header = ctk.CTkFrame(scroll_frame, fg_color="#051622")
    header.pack(fill="x")
    for col in df.columns:
        ctk.CTkLabel(header, text=str(col), width=col_width, anchor="center",
                     font=("Courier New", 13, "bold"), text_color="#00fff0").pack(side="left", padx=2, pady=5)

    # rows
    for _, row in df.iterrows():
        row_frame = ctk.CTkFrame(scroll_frame, fg_color="#0b1a24")
        row_frame.pack(fill="x", pady=2)
        for val in row:
            ctk.CTkLabel(row_frame, text=str(val), width=col_width, anchor="center",
                         text_color="#00fff0", font=("Courier New", 12)).pack(side="left", padx=2, pady=3)


# ===================== ACCOUNTS SECTION (top-level) =====================
def build_accounts_section(parent, USERID):
    """Create Accounts UI inside parent. CRUD operations refresh the content area."""
    title = ctk.CTkLabel(parent, text="🏦 Your Accounts", text_color="#03e9f4",
                         font=("Courier New", 18, "bold"))
    title.pack(pady=10)

    # content frame where table will render
    content_frame = ctk.CTkFrame(parent, fg_color="#0b1a24")
    content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Buttons area (kept visible)
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
        add_win.configure(fg_color="#0b1a24")

        labels = ["Account ID", "Name", "Type", "Current Balance"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=6)
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0", width=300)
            ent.pack()
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
        update_win.configure(fg_color="#0b1a24")

        ctk.CTkLabel(update_win, text="Account ID", text_color="#00fff0").pack(pady=6)
        a_ent = ctk.CTkEntry(update_win, fg_color="#051622", text_color="#00fff0", width=280)
        a_ent.pack()
        ctk.CTkLabel(update_win, text="New Balance", text_color="#00fff0").pack(pady=6)
        b_ent = ctk.CTkEntry(update_win, fg_color="#051622", text_color="#00fff0", width=280)
        b_ent.pack()

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

    # Buttons (kept separate so table area can be the content_frame)
    ctk.CTkButton(btn_frame, text="Add Account", command=add_account,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=140).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Update Balance", command=update_balance,
                  fg_color="#051622", text_color="#00fff0", corner_radius=20, width=140).pack(side="left", padx=8)
    ctk.CTkButton(btn_frame, text="Delete Account", command=delete_account,
                  fg_color="#051622", text_color="#ff4444", corner_radius=20, width=140).pack(side="left", padx=8)

    # initial load
    fetch_accounts()


# ===================== TRANSACTIONS SECTION (top-level) =====================
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
        add_win.configure(fg_color="#0b1a24")

        labels = ["Transaction ID", "Account ID", "Category ID", "Expense Amount", "Mode (cash/card)", "Time (YYYY-MM-DD HH:MM:SS)"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=6)
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0", width=300)
            ent.pack()
            entries[lbl] = ent

        def save_transaction():
            vals = [entries[l].get().strip() for l in labels]
            if not vals[0] or not vals[1] or not vals[3]:
                messagebox.showwarning("Missing", "TXID, Account ID and Expense are required.")
                return
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cur = conn.cursor()

                # 🟢 Show OLD balance (uses your GetAccountBalance function)
                cur.execute("SELECT GetAccountBalance(%s)", (vals[1],))
                old_bal = cur.fetchone()[0]
                messagebox.showinfo("Before Transaction", f"Current Balance: ₹{old_bal:.2f}")

                # 🟢 Insert transaction (this triggers trg_update_account_balance_simple automatically)
                cur.execute("""
                    INSERT INTO `Transaction` (TXID, ACCID, CID, expense, mode, time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, tuple(vals))

                conn.commit()

                # 🟢 Show NEW balance after trigger fires
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

    


# ===================== GOALS SECTION (top-level) =====================
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
        add_win.configure(fg_color="#0b1a24")

        labels = ["Goal ID", "Title", "Target Amount", "Deadline (YYYY-MM-DD)"]
        entries = {}
        for lbl in labels:
            ctk.CTkLabel(add_win, text=lbl, text_color="#00fff0").pack(pady=6)
            ent = ctk.CTkEntry(add_win, fg_color="#051622", text_color="#00fff0", width=300)
            ent.pack()
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


# ===================== BUDGET SECTION (top-level) =====================
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


# ===================== MAIN USER DASHBOARD ENTRY =====================
def open_user_dashboard(USERID, user_name):
    win = ctk.CTkToplevel()
    win.title(f"Finance Tracker - {user_name}")
    win.geometry("1000x600")
    win.configure(fg_color="#0b1a24")

    # sidebar
    sidebar = ctk.CTkFrame(win, width=200, fg_color="#051622", corner_radius=0)
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text=f"👤 {user_name}", text_color="#00fff0",
                 font=("Courier New", 16, "bold")).pack(pady=20)

    # main area
    main_frame = ctk.CTkFrame(win, fg_color="#0b1a24")
    main_frame.pack(side="right", expand=True, fill="both", padx=8, pady=8)

    # utility to clear main_frame when switching sections
    def clear_main():
        for w in main_frame.winfo_children():
            w.destroy()

    # link the sidebar buttons to top-level builders
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

    # sidebar buttons
    btns = [
        ("🏦 Accounts", open_accounts),
        ("💸 Transactions", open_transactions),
        ("🎯 Goals", open_goals),
        ("📈 Budgets", open_budgets),
        ("🚪 Logout", win.destroy),
    ]
    for text, cmd in btns:
        ctk.CTkButton(sidebar, text=text, command=cmd, width=170, fg_color="#051622",
                      text_color="#00fff0", hover_color="#03e9f4", corner_radius=15,
                      font=("Courier New", 13, "bold")).pack(pady=8)

    # default view
    build_accounts_section(main_frame, USERID)
