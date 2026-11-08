import tkinter as tk
from tkinter import ttk, messagebox
from db import connect, session

window = tk.Tk()
window.title("Login")
window.geometry("350x330")
window.resizable(False, False)

tk.Label(window, text="FDRE TVTI", bg="#1F3A5F", fg="white",
 font=("Arial", 18, "bold"), pady=12).pack(fill="x")
tk.Label(window, text="Student Information Management System",
 font=("Arial", 11), pady=10).pack()

ttk.Label(window, text="Username").pack(pady=(10, 2))
entry_user = ttk.Entry(window, width=25)
entry_user.pack()

ttk.Label(window, text="Password").pack(pady=(10, 2))
entry_pass = ttk.Entry(window, width=25, show="*")
entry_pass.pack()

def login(event=None):
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
     (entry_user.get(), entry_pass.get()))
    user = cursor.fetchone()
    db.close()
    if user:
        session["user"] = entry_user.get()
        window.destroy()
        import main
    else:
        messagebox.showerror("Error", "Wrong username or password")

ttk.Button(window, text="Login", width=15, command=login).pack(pady=25)
entry_pass.bind("<Return>", login)

window.mainloop()