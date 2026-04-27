import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3  # This handles the permanent database

root = tk.Tk()
root.title("Federal Urdu University Admission Form")
root.geometry("1000x950")
root.config(bg="#f0f0f0")

records = []
current_index = -1

# =========================
# DATABASE INITIALIZATION
# =========================
def init_db():
    # This creates the 'admission.db' file in your folder automatically
    conn = sqlite3.connect("admission.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students 
                      (form_no TEXT, date TEXT, name TEXT, father TEXT, 
                       cnic TEXT, gender TEXT, phone TEXT, dob TEXT, address TEXT)''')
    conn.commit()
    conn.close()

# Run database setup at startup
init_db()

# =========================
# REINFORCED STYLING FOR LINES
# =========================
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", fieldbackground="white", foreground="black", rowheight=30, borderwidth=1)
style.map("Treeview", background=[('selected', '#347083')], foreground=[('selected', 'white')])
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background="#e1e1e1")

# =========================
# FUNCTIONS
# =========================
def save():
    global current_index
    data = {label: entry.get() for label, entry in main_entries}
    
    if not data["Name"] or not data["Form No"]:
        messagebox.showwarning("Warning", "Name and Form No are required to save.")
        return

    # 1. SAVE PERMANENTLY TO SQLITE DATABASE
    conn = sqlite3.connect("admission.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?)", 
                   (data["Form No"], data["Date"], data["Name"], data["Father's Name"], 
                    data["CNIC No"], data["Gender"], data["Phone"], data["Date of Birth"], data["Postal Address"]))
    conn.commit()
    conn.close()

    # 2. SAVE TO TEMPORARY LIST (For Next/Prev buttons)
    records.append(data)
    current_index = len(records) - 1
    update_counter()
    
    messagebox.showinfo("Saved", "Record saved to Database permanently!")
    clear_form()

def clear_form():
    for _, entry in main_entries:
        entry.delete(0, tk.END)

def display_record(index):
    if 0 <= index < len(records):
        record = records[index]
        for label, entry in main_entries:
            entry.delete(0, tk.END)
            entry.insert(0, record.get(label, ""))
        update_counter()

def next_record():
    global current_index
    if current_index < len(records) - 1:
        current_index += 1
        display_record(current_index)

def prev_record():
    global current_index
    if current_index > 0:
        current_index -= 1
        display_record(current_index)

def update_counter():
    text = f"Record: {current_index + 1} of {len(records)}" if records else "No Records"
    counter_label.config(text=text)

# =========================
# UI HEADER
# =========================
header_frame = tk.Frame(root, bg="white", pady=10)
header_frame.pack(fill="x")
tk.Label(header_frame, text="FEDERAL URDU UNIVERSITY OF ARTS, SCIENCE & TECHNOLOGY", 
         font=("Arial", 14, "bold"), bg="white").pack()
tk.Label(header_frame, text="Academic Session 2025 - Application Form", 
         font=("Arial", 12, "italic"), bg="white", fg="#333").pack()
tk.Label(header_frame, text="Bachelor Programmes (Evening)", 
         font=("Arial", 10), bg="white").pack()

# =========================
# MAIN CONTAINER
# =========================
container = tk.Frame(root, bg="#f0f0f0", padx=20)
container.pack(fill="both", expand=True)

info_frame = tk.LabelFrame(container, text="Personal Information", bg="white", padx=10, pady=10)
info_frame.pack(fill="x", pady=10)

fields = [
    ("Form No", 0, 0), ("Date", 0, 2),
    ("Name", 1, 0), ("Father's Name", 1, 2),
    ("CNIC No", 2, 0), ("Gender", 2, 2),
    ("Phone", 3, 0), ("Date of Birth", 3, 2),
    ("Postal Address", 4, 0)
]

main_entries = []
for label, r, c in fields:
    tk.Label(info_frame, text=label, bg="white").grid(row=r, column=c, sticky="w", pady=5)
    width = 25 if label != "Postal Address" else 75
    entry = tk.Entry(info_frame, width=width, relief="solid", borderwidth=1)
    col_span = 1 if label != "Postal Address" else 3
    entry.grid(row=r, column=c+1, columnspan=col_span, sticky="w", padx=10)
    main_entries.append((label, entry))

# Qualifications and Choice tables remain for visual representation
qual_frame = tk.LabelFrame(container, text="Qualifications", bg="white", padx=10, pady=10)
qual_frame.pack(fill="x", pady=5)
qual_cols = ("Examination", "Group", "Roll No", "Board", "Year", "Obtained", "Total")
tree_qual = ttk.Treeview(qual_frame, columns=qual_cols, show="headings", height=2)
for col in qual_cols:
    tree_qual.heading(col, text=col)
    tree_qual.column(col, width=120, anchor="center")
tree_qual.insert("", "end", values=("S.S.C", "Science", "932047", "Karachi", "2018", "554", "850"))
tree_qual.insert("", "end", values=("H.S.C", "Pre-Medical", "915812", "Karachi", "2021", "546", "1100"))
tree_qual.pack(fill="x")

choice_frame = tk.LabelFrame(container, text="Order of Choices", bg="white", padx=10, pady=10)
choice_frame.pack(fill="x", pady=5)
choice_cols = ("Priority", "Discipline / Department", "Campus")
tree_choice = ttk.Treeview(choice_frame, columns=choice_cols, show="headings", height=3)
for col in choice_cols:
    tree_choice.heading(col, text=col)
    tree_choice.column(col, width=300, anchor="center")
for row in [("01", "Biotechnology", "Gulshan-e-Iqbal"), ("02", "Botany", "Gulshan-e-Iqbal")]:
    tree_choice.insert("", "end", values=row)
tree_choice.pack(fill="x")

# =========================
# NAVIGATION & FOOTER
# =========================
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="SAVE", bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=12, command=save).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="PREVIOUS", bg="#007bff", fg="white", width=12, command=prev_record).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="NEXT", bg="#007bff", fg="white", width=12, command=next_record).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="CLEAR", bg="#dc3545", fg="white", width=12, command=clear_form).grid(row=0, column=3, padx=5)

counter_label = tk.Label(root, text="No Records", bg="#f0f0f0", font=("Arial", 10, "italic"))
counter_label.pack(pady=5)

root.mainloop()