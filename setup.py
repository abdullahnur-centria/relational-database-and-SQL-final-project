import mysql.connector

# 1. Connect to your new DBngin server (it has no password by default!)
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="" 
)
cursor = db.cursor()

# 2. Create the database
cursor.execute("CREATE DATABASE IF NOT EXISTS warehouse_db")
cursor.execute("USE warehouse_db")

# 3. Create the tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    contact_person VARCHAR(100)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    stock_count INT,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
)""")

# 4. Put one fake supplier in so we have data to look at
cursor.execute("SELECT * FROM suppliers")
if not cursor.fetchall():
    cursor.execute("INSERT INTO suppliers (company_name, contact_person) VALUES ('Global Tech', 'Alice Smith')")
    db.commit()

print("✅ SUCCESS: Database and tables are perfectly set up!")
db.close()