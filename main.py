import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from db import connect, session

window = tk.Tk()
window.title("FDRE TVTI Student Information Management System")
window.geometry("1200x700")
window.minsize(1100, 600)

header = tk.Frame(window, bg="#1F3A5F")
header.pack(fill="x")
tk.Label(header, text="FDRE TVTI Student Information Management System",
         bg="#1F3A5F", fg="white", font=("Arial", 18, "bold"), pady=15).pack(side="left", padx=20)


form = ttk.LabelFrame(window, text="Student Information")
form.pack(fill="x", padx=20, pady=15)

ttk.Label(form, text="Student ID (ttbr/934/16)").grid(row=0, column=0, padx=15, pady=8, sticky="w")
entry_id = ttk.Entry(form, width=25)
entry_id.grid(row=0, column=1, padx=15, pady=8)

ttk.Label(form, text="Full Name").grid(row=1, column=0, padx=15, pady=8, sticky="w")
entry_name = ttk.Entry(form, width=25)
entry_name.grid(row=1, column=1, padx=15, pady=8)

ttk.Label(form, text="Gender").grid(row=2, column=0, padx=15, pady=8, sticky="w")
combo_gender = ttk.Combobox(form, width=22, values=["Male", "Female"], state="readonly")
combo_gender.grid(row=2, column=1, padx=15, pady=8)

ttk.Label(form, text="Phone").grid(row=3, column=0, padx=15, pady=8, sticky="w")
entry_phone = ttk.Entry(form, width=25)
entry_phone.grid(row=3, column=1, padx=15, pady=8)

ttk.Label(form, text="GPA (0 - 4)").grid(row=4, column=0, padx=15, pady=8, sticky="w")
entry_gpa = ttk.Entry(form, width=25)
entry_gpa.grid(row=4, column=1, padx=15, pady=8)

ttk.Label(form, text="Age").grid(row=0, column=2, padx=15, pady=8, sticky="w")
entry_age = ttk.Entry(form, width=25)
entry_age.grid(row=0, column=3, padx=15, pady=8)

ttk.Label(form, text="Department").grid(row=1, column=2, padx=15, pady=8, sticky="w")
combo_dept = ttk.Combobox(form, width=35, values=["Construction Technology", "Surveying Technology", "Road Technology", "Water Construction Technology", "Architectural Design Technology", "Wood Technology", "Automotive Technology", "Manufacturing Technology", "Electrical and Electronics Technology", "Information and Communication Technology (ICT)", "Garment Technology", "Freshman Course"], state="readonly")
combo_dept.grid(row=1, column=3, padx=15, pady=8)

ttk.Label(form, text="Year").grid(row=2, column=2, padx=15, pady=8, sticky="w")
combo_year = ttk.Combobox(form, width=22, values=["Year 1", "Year 2", "Year 3", "Year 4"], state="readonly")
combo_year.grid(row=2, column=3, padx=15, pady=8)

ttk.Label(form, text="Semester").grid(row=3, column=2, padx=15, pady=8, sticky="w")
combo_semester = ttk.Combobox(form, width=22, values=["Semester 1", "Semester 2"], state="readonly")
combo_semester.grid(row=3, column=3, padx=15, pady=8)

buttons = tk.Frame(window)
buttons.pack(pady=5)


search_bar = tk.Frame(window)
search_bar.pack(pady=5)
ttk.Label(search_bar, text="Search (ID, name or department)").pack(side="left", padx=10)
entry_search = ttk.Entry(search_bar, width=30)
entry_search.pack(side="left", padx=10)

table_frame = tk.Frame(window)
table_frame.pack(fill="both", expand=True, padx=20, pady=15)

table = ttk.Treeview(table_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8", "9"), show="headings")
table.heading("1", text="ID")
table.heading("2", text="Name")
table.heading("3", text="Gender")
table.heading("4", text="Age")
table.heading("5", text="Department")
table.heading("6", text="Year")
table.heading("7", text="Phone")
table.heading("8", text="Semester")
table.heading("9", text="GPA")
table.column("1", width=120)
table.column("2", width=170)
table.column("3", width=70)
table.column("4", width=50)
table.column("5", width=260)
table.column("6", width=70)
table.column("7", width=110)
table.column("8", width=100)
table.column("9", width=60)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
table.pack(side="left", fill="both", expand=True)

def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    combo_gender.set("")
    entry_age.delete(0, tk.END)
    combo_dept.set("")
    combo_year.set("")
    entry_phone.delete(0, tk.END)
    combo_semester.set("")
    entry_gpa.delete(0, tk.END)

def gpa_is_correct():
    """GPA must be a number from 0 to 4."""
    try:
        gpa = float(entry_gpa.get())
    except ValueError:
        return False
    return 0 <= gpa <= 4

def view_all():
    entry_search.delete(0, tk.END)
    for item in table.get_children():
        table.delete(item)
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        table.insert("", tk.END, values=row)
    db.close()

def search_students(event=None):
    word = "%" + entry_search.get() + "%"
    for item in table.get_children():
        table.delete(item)
    db = connect()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM students WHERE student_id LIKE ?
                      OR full_name LIKE ? OR department LIKE ?""", (word, word, word))
    for row in cursor.fetchall():
        table.insert("", tk.END, values=row)
    db.close()

def add_student():
    student_id = entry_id.get().lower()
    if student_id.count("/") != 2:
        messagebox.showwarning("Warning", "ID must look like ttbr/934/16")
        return
    if not gpa_is_correct():
        messagebox.showwarning("Warning", "GPA must be a number from 0 to 4")
        return
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (student_id, entry_name.get(), combo_gender.get(), entry_age.get(),
                        combo_dept.get(), combo_year.get(), entry_phone.get(),
                        combo_semester.get(), entry_gpa.get()))
        db.commit()
        db.close()
        clear_fields()
        view_all()
    except Exception as error:
        messagebox.showerror("Error", str(error))

def select_student(event):
    selected = table.selection()
    if selected == ():
        return
    student_id = str(table.item(selected[0])["values"][0])
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    row = cursor.fetchone()
    db.close()
    clear_fields()
    entry_id.insert(0, row[0])
    entry_name.insert(0, row[1])
    combo_gender.set(row[2])
    entry_age.insert(0, row[3])
    combo_dept.set(row[4])
    combo_year.set(row[5])
    entry_phone.insert(0, row[6])
    combo_semester.set(row[7])
    entry_gpa.insert(0, str(row[8]))

def update_student():
    if not gpa_is_correct():
        messagebox.showwarning("Warning", "GPA must be a number from 0 to 4")
        return
    try:
        db = connect()
        cursor = db.cursor()
        cursor.execute("""UPDATE students SET full_name=?, gender=?, age=?,
                          department=?, level=?, phone=?, semester=?, gpa=?
                          WHERE student_id=?""",
                       (entry_name.get(), combo_gender.get(), entry_age.get(),
                        combo_dept.get(), combo_year.get(), entry_phone.get(),
                        combo_semester.get(), entry_gpa.get(), entry_id.get()))
        db.commit()
        db.close()
        clear_fields()
        view_all()
    except Exception as error:
        messagebox.showerror("Error", str(error))

def delete_student():
    if messagebox.askyesno("Confirm", "Delete this student?"):
        db = connect()
        cursor = db.cursor()
        cursor.execute("DELETE FROM students WHERE student_id=?", (entry_id.get(),))
        db.commit()
        db.close()
        clear_fields()
        view_all()

def change_password():
    box = tk.Toplevel(window)
    box.title("Change Password")
    box.geometry("320x330")
    box.resizable(False, False)

    ttk.Label(box, text="Old password").pack(pady=(15, 2))
    entry_old = ttk.Entry(box, width=25, show="*")
    entry_old.pack()

    ttk.Label(box, text="New password").pack(pady=(10, 2))
    entry_new = ttk.Entry(box, width=25, show="*")
    entry_new.pack()

    ttk.Label(box, text="Confirm new password").pack(pady=(10, 2))
    entry_again = ttk.Entry(box, width=25, show="*")
    entry_again.pack()

    def save_password():
        if entry_new.get() == "":
            messagebox.showwarning("Warning", "New password cannot be empty", parent=box)
            return
        if entry_new.get() != entry_again.get():
            messagebox.showwarning("Warning", "The two new passwords are not the same", parent=box)
            return
        db = connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (session["user"], entry_old.get()))
        if cursor.fetchone() is None:
            db.close()
            messagebox.showerror("Error", "Old password is wrong", parent=box)
            return
        cursor.execute("UPDATE users SET password=? WHERE username=?",
                       (entry_new.get(), session["user"]))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Password changed", parent=box)
        box.destroy()

    ttk.Button(box, text="Save", width=15, command=save_password).pack(pady=25)

def logout():
    if messagebox.askyesno("Logout", "Do you want to log out?"):
        window.destroy()
        
        if getattr(sys, "frozen", False):
            os.environ["PYINSTALLER_RESET_ENVIRONMENT"] = "1"
            os.execl(sys.executable, sys.executable)
        else:
            login_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login.py")
            os.execl(sys.executable, sys.executable, login_file)

ttk.Button(buttons, text="Add", width=15, command=add_student).pack(side="left", padx=10)
ttk.Button(buttons, text="Update", width=15, command=update_student).pack(side="left", padx=10)
ttk.Button(buttons, text="Delete", width=15, command=delete_student).pack(side="left", padx=10)
ttk.Button(buttons, text="Clear", width=15, command=clear_fields).pack(side="left", padx=10)

ttk.Button(search_bar, text="Search", width=12, command=search_students).pack(side="left", padx=5)
ttk.Button(search_bar, text="Show All", width=12, command=view_all).pack(side="left", padx=5)
entry_search.bind("<Return>", search_students)

ttk.Button(header, text="Logout", width=10, command=logout).pack(side="right", padx=15)
ttk.Button(header, text="Change Password", width=16, command=change_password).pack(side="right")

table.bind("<<TreeviewSelect>>", select_student)
view_all()
window.mainloop()