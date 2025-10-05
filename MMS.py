# Paste the full MMS Python code here
from tkinter import *
from tkinter import messagebox, filedialog
import os, csv

# Ensure database file exists
DB_FILE = "database_proj"
if not os.path.exists(DB_FILE):
    open(DB_FILE, 'w').close()

# --- Utility Functions ---
def read_database():
    with open(DB_FILE, 'r') as f:
        return [line.strip().split() for line in f if line.strip()]

def write_database(data):
    with open(DB_FILE, 'w') as f:
        for record in data:
            f.write(" ".join(record) + "\n")

def update_history():
    history_text.delete(1.0, END)
    for line in read_database():
        history_text.insert(END, " | ".join(line) + "\n")

def clear_entries(entries):
    for e in entries:
        e.delete(0, END)

def update_entries(entries, values):
    clear_entries(entries)
    for i, val in enumerate(values):
        if i < len(entries):
            entries[i].insert(0, str(val))

# --- CRUD Functions ---
def add_item():
    values = [e.get().strip() for e in main_entries]
    if any(not v for v in values):
        messagebox.showerror("Error", "Please fill all fields")
        return
    data = read_database()
    data.append(values)
    write_database(data)
    update_history()
    clear_entries(main_entries)

def delete_item():
    name = entry1.get().strip()
    if not name:
        messagebox.showerror("Error", "Enter item name to delete")
        return
    data = [rec for rec in read_database() if rec[0] != name]
    write_database(data)
    update_history()
    clear_entries(main_entries)

def update_item():
    name = entry1.get().strip()
    data = read_database()
    updated = False
    new_values = [e.get().strip() for e in main_entries]
    for i, rec in enumerate(data):
        if rec[0] == name:
            data[i] = new_values
            updated = True
            break
    if updated:
        write_database(data)
        update_history()
        clear_entries(main_entries)
    else:
        messagebox.showinfo("Not Found", "Item not found")

def search_item():
    query = entry_search.get().strip().lower()
    if not query:
        messagebox.showinfo("Search", "Enter search query")
        return
    found = False
    for rec in read_database():
        if any(query in field.lower() for field in rec):
            update_entries(main_entries, rec)
            found = True
            break
    if not found:
        messagebox.showinfo("Not Found", "Item not found")

def total_stock_value():
    total = 0
    for rec in read_database():
        try:
            price = float(rec[1])
            qty = int(rec[2])
            total += price * qty
        except:
            continue
    messagebox.showinfo("Total Stock Value", f"Total = {total}")

def export_csv():
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
    if not path:
        return
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(read_database())
    messagebox.showinfo("Exported", f"Database exported to {path}")

def first_item():
    data = read_database()
    if data:
        update_entries(main_entries, data[0])

def last_item():
    data = read_database()
    if data:
        update_entries(main_entries, data[-1])

def previous_item():
    current = [e.get().strip() for e in main_entries]
    data = read_database()
    prev = None
    for rec in data:
        if rec == current:
            break
        prev = rec
    if prev:
        update_entries(main_entries, prev)
    else:
        messagebox.showinfo("Info", "This is the first item")

def next_item():
    current = [e.get().strip() for e in main_entries]
    data = read_database()
    for i, rec in enumerate(data):
        if rec == current and i + 1 < len(data):
            update_entries(main_entries, data[i + 1])
            return
    messagebox.showinfo("Info", "This is the last item")

# --- GUI ---
root = Tk()
root.title("Medical Management System")
root.configure(bg='black')

Label(root, text="MEDICAL MANAGEMENT SYSTEM", bg="black", fg="white", font=("Times", 30)).grid(row=0, column=0, columnspan=6, pady=10)

# Main entries
labels_main = ["Item Name", "Price", "Quantity", "Category", "Discount"]
main_entries = []
for i, text in enumerate(labels_main):
    Label(root, text=text, bg="red", fg="white", font=("Times",12), width=25).grid(row=i+1, column=0, sticky=W, padx=10, pady=5)
    e = Entry(root, font=("Times",12))
    e.grid(row=i+1, column=1, padx=10, pady=5)
    main_entries.append(e)
entry1, entry2, entry3, entry4, entry5 = main_entries

# Search
Label(root, text="Search Item", bg="red", fg="white", font=("Times",12), width=25).grid(row=6, column=0, sticky=W, padx=10, pady=5)
entry_search = Entry(root, font=("Times",12))
entry_search.grid(row=6, column=1, padx=10, pady=5)
Button(root, text="SEARCH", command=search_item).grid(row=6, column=2)

# Buttons
Button(root, text="ADD ITEM", command=add_item).grid(row=1, column=4)
Button(root, text="DELETE ITEM", command=delete_item).grid(row=2, column=4)
Button(root, text="UPDATE ITEM", command=update_item).grid(row=3, column=4)
Button(root, text="FIRST ITEM", command=first_item).grid(row=4, column=4)
Button(root, text="LAST ITEM", command=last_item).grid(row=5, column=4)
Button(root, text="PREVIOUS ITEM", command=previous_item).grid(row=1, column=5)
Button(root, text="NEXT ITEM", command=next_item).grid(row=2, column=5)
Button(root, text="SHOW HISTORY", command=update_history).grid(row=3, column=5)
Button(root, text="TOTAL STOCK VALUE", command=total_stock_value).grid(row=4, column=5)
Button(root, text="EXPORT CSV", command=export_csv).grid(row=5, column=5)

# History Text
history_text = Text(root, width=60, height=20)
history_text.grid(row=7, column=0, columnspan=6, padx=10, pady=10)
update_history()

root.mainloop()
