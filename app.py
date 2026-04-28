import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Connect to DBngin server
def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="", 
        database="warehouse_db"
    )

def add_product():
    name = entry_name.get()
    stock = entry_stock.get()
    
    # 1. This is INSERT command requirement
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO products (product_name, stock_count, supplier_id) VALUES (%s, %s, 1)", (name, stock))
    db.commit()
    messagebox.showinfo("Success", f"Added '{name}' to inventory!")
    
    entry_name.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    db.close()

def show_inventory():
    # 2. This is JOIN requirement (combining 2 tables)
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT p.product_name, p.stock_count, s.company_name 
    FROM products p
    JOIN suppliers s ON p.supplier_id = s.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Clear the table and show the new data
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("", "end", values=row)
    db.close()

# --- Build the visual window ---
root = tk.Tk()
root.title("Final Project: Warehouse Manager")
root.geometry("450x400")

tk.Label(root, text="New Product Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="How many in stock?:").pack(pady=5)
entry_stock = tk.Entry(root)
entry_stock.pack()

tk.Button(root, text="Add Product (INSERT)", command=add_product).pack(pady=10)
tk.Button(root, text="Show Inventory (JOIN)", command=show_inventory).pack(pady=5)

# The table that displays the data
columns = ("Product", "Stock", "Supplier")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)
tree.pack(pady=20)

root.mainloop()
