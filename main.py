import tkinter as tk
from tkinter import messagebox
import sqlite3
from scanner import scan_barcode

# ---------------- DATABASE ---------------- #

def create_database():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        barcode TEXT PRIMARY KEY,
        product_name TEXT,
        brand_name TEXT
    )
    """)

    conn.commit()
    conn.close()

create_database()

# ---------------- ADD PRODUCT ---------------- #

def open_add_product():

    add_window = tk.Toplevel(app)
    add_window.title("Add Product")
    add_window.geometry("400x350")

    tk.Label(add_window, text="Barcode").pack(pady=5)
    barcode_entry = tk.Entry(add_window, width=30)
    barcode_entry.pack()

    tk.Label(add_window, text="Product Name").pack(pady=5)
    product_entry = tk.Entry(add_window, width=30)
    product_entry.pack()

    tk.Label(add_window, text="Brand Name").pack(pady=5)
    brand_entry = tk.Entry(add_window, width=30)
    brand_entry.pack()

    def scan_and_fill():
        code = scan_barcode()

        if code:
            barcode_entry.delete(0, tk.END)
            barcode_entry.insert(0, code)

    def save_product():

        barcode = barcode_entry.get()
        product = product_entry.get()
        brand = brand_entry.get()

        if not barcode or not product or not brand:
            messagebox.showerror(
                "Error",
                "Fill all fields"
            )
            return

        try:
            conn = sqlite3.connect("products.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO products VALUES (?, ?, ?)",
                (barcode, product, brand)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Product Saved Successfully"
            )

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Barcode Already Exists"
            )

    tk.Button(
        add_window,
        text="Scan Barcode",
        command=scan_and_fill
    ).pack(pady=10)

    tk.Button(
        add_window,
        text="Save Product",
        command=save_product
    ).pack(pady=10)

# ---------------- VIEW PRODUCTS ---------------- #

def view_products():

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    window = tk.Toplevel(app)
    window.title("Products")
    window.geometry("600x400")

    text = tk.Text(window)
    text.pack(fill="both", expand=True)

    for product in products:
        text.insert(
            tk.END,
            f"Barcode: {product[0]}\n"
            f"Product: {product[1]}\n"
            f"Brand: {product[2]}\n\n"
        )

# ---------------- VERIFY PRODUCT ---------------- #

def verify_product():

    code = scan_barcode()

    if not code:
        return

    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE barcode=?",
        (code,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        messagebox.showinfo(
            "ORIGINAL",
            f"Product : {result[1]}\nBrand : {result[2]}"
        )

    else:

        messagebox.showerror(
            "FAKE PRODUCT",
            "Product Not Found In Database"
        )

# ---------------- SCAN BARCODE ---------------- #

def scan_product():

    code = scan_barcode()

    if code:
        messagebox.showinfo(
            "Barcode Detected",
            code
        )

# ---------------- DASHBOARD ---------------- #

def open_dashboard():

    dashboard = tk.Toplevel(app)
    dashboard.title("Admin Dashboard")
    dashboard.geometry("500x450")

    tk.Label(
        dashboard,
        text="ADMIN DASHBOARD",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        dashboard,
        text="Scan Barcode",
        width=20,
        height=2,
        command=scan_product
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Add Product",
        width=20,
        height=2,
        command=open_add_product
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="View Products",
        width=20,
        height=2,
        command=view_products
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Logout",
        width=20,
        height=2,
        command=dashboard.destroy
    ).pack(pady=10)

# ---------------- ADMIN LOGIN ---------------- #

def open_admin():

    login_window = tk.Toplevel(app)
    login_window.title("Admin Login")
    login_window.geometry("400x300")

    tk.Label(
        login_window,
        text="ADMIN LOGIN",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def check_login():

        if (
            username_entry.get() == "admin"
            and
            password_entry.get() == "admin123"
        ):

            login_window.destroy()
            open_dashboard()

        else:

            messagebox.showerror(
                "Error",
                "Invalid Username or Password"
            )

    tk.Button(
        login_window,
        text="LOGIN",
        command=check_login
    ).pack(pady=20)

# ---------------- USER LOGIN ---------------- #

def open_user():

    user_window = tk.Toplevel(app)
    user_window.title("User Verification")
    user_window.geometry("400x300")

    tk.Label(
        user_window,
        text="PRODUCT VERIFICATION",
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    tk.Label(
        user_window,
        text="Enter Barcode"
    ).pack()

    barcode_entry = tk.Entry(
        user_window,
        width=30
    )
    barcode_entry.pack(pady=10)

    def scan_fill():

        code = scan_barcode()

        if code:
            barcode_entry.delete(0, tk.END)
            barcode_entry.insert(0, code)

    def verify_manual():

        code = barcode_entry.get()

        if not code:
            messagebox.showerror(
                "Error",
                "Enter or Scan Barcode"
            )
            return

        conn = sqlite3.connect("products.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM products WHERE barcode=?",
            (code,)
        )

        result = cursor.fetchone()

        conn.close()

        if result:

         messagebox.showinfo(
        "ORIGINAL PRODUCT",
        f"✅ ORIGINAL PRODUCT\n\n"
        f"Product : {result[1]}\n"
        f"Brand : {result [2]}"
    )

        else:

         messagebox.showerror(
        "FAKE PRODUCT",
        "❌ Product Authentication Failed\n\n"
        "Product Not Found In Database"
    )
    tk.Button(
        user_window,
        text="Scan Barcode",
        width=20,
        command=scan_fill
    ).pack(pady=10)

    tk.Button(
        user_window,
        text="Verify Product",
        width=20,
        command=verify_manual
    ).pack(pady=10)

# ---------------- MAIN WINDOW ---------------- #

app = tk.Tk()

app.title("SMART FAKE PRODUCT DETECTION SYSTEM")
app.geometry("700x500")
app.resizable(False, False)

tk.Label(
    app,
    text="SMART FAKE PRODUCT DETECTION SYSTEM",
    font=("Arial", 18, "bold")
).pack(pady=50)

tk.Label(
    app,
    text="Select Login Type",
    font=("Arial", 14)
).pack(pady=20)

tk.Button(
    app,
    text="ADMIN LOGIN",
    width=20,
    height=2,
    command=open_admin
).pack(pady=10)

tk.Button(
    app,
    text="USER LOGIN",
    width=20,
    height=2,
    command=open_user
).pack(pady=10)

tk.Button(
    app,
    text="EXIT",
    width=20,
    height=2,
    command=app.destroy
).pack(pady=30)

app.mainloop()