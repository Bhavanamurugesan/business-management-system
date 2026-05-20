from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# =========================
# DATABASE SETUP
# =========================

conn = sqlite3.connect('database.db')

conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT
    )
    '''
)

conn.commit()


# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return render_template('index.html')


# =========================
# CUSTOMER MODULE
# =========================

@app.route('/customers')
def customers():

    conn = sqlite3.connect('database.db')

    cursor = conn.execute("SELECT * FROM customer")

    data = cursor.fetchall()

    return render_template(
        'customers.html',
        customers=data
    )


@app.route('/add_customer', methods=['POST'])
def add_customer():

    try:

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "INSERT INTO customer(name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email)
        )

        conn.commit()

        return render_template(
            'success.html',
            message="Customer Added Successfully"
        )

    except:

        return "Error Adding Customer"


@app.route('/delete_customer/<int:id>')
def delete_customer(id):

    conn = sqlite3.connect('database.db')

    conn.execute(
        "DELETE FROM customer WHERE id=?",
        (id,)
    )

    conn.commit()

    return render_template(
        'success.html',
        message="Customer Deleted Successfully"
    )


@app.route('/edit_customer/<int:id>')
def edit_customer(id):

    conn = sqlite3.connect('database.db')

    cursor = conn.execute(
        "SELECT * FROM customer WHERE id=?",
        (id,)
    )

    customer = cursor.fetchone()

    return render_template(
        'edit_customer.html',
        customer=customer
    )


@app.route('/update_customer/<int:id>', methods=['POST'])
def update_customer(id):

    try:

        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "UPDATE customer SET name=?, phone=?, email=? WHERE id=?",
            (name, phone, email, id)
        )

        conn.commit()

        return render_template(
            'success.html',
            message="Customer Updated Successfully"
        )

    except:

        return "Error Updating Customer"


# =========================
# PRODUCT MODULE
# =========================

@app.route('/products')
def products():

    conn = sqlite3.connect('database.db')

    cursor = conn.execute(
        "SELECT * FROM products"
    )

    data = cursor.fetchall()

    return render_template(
        'products.html',
        products=data
    )


@app.route('/add_product', methods=['POST'])
def add_product():

    try:

        product_name = request.form['product_name']
        quantity = request.form['quantity']
        price = request.form['price']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "INSERT INTO products(product_name, quantity, price) VALUES (?, ?, ?)",
            (product_name, quantity, price)
        )

        conn.commit()

        return render_template(
            'success.html',
            message="Product Added Successfully"
        )

    except:

        return "Error Adding Product"


@app.route('/delete_product/<int:id>')
def delete_product(id):

    conn = sqlite3.connect('database.db')

    conn.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()

    return render_template(
        'success.html',
        message="Product Deleted Successfully"
    )


@app.route('/edit_product/<int:id>')
def edit_product(id):

    conn = sqlite3.connect('database.db')

    cursor = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (id,)
    )

    product = cursor.fetchone()

    return render_template(
        'edit_product.html',
        product=product
    )


@app.route('/update_product/<int:id>', methods=['POST'])
def update_product(id):

    try:

        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "UPDATE products SET product_name=?, quantity=?, price=? WHERE id=?",
            (name, quantity, price, id)
        )

        conn.commit()

        return redirect('/products')

    except:

        return "Error Updating Product"


# =========================
# SALES MODULE
# =========================

@app.route('/sales')
def sales():

    conn = sqlite3.connect('database.db')

    cursor = conn.execute(
        "SELECT * FROM sales"
    )

    data = cursor.fetchall()

    cursor2 = conn.execute(
        "SELECT SUM(total) FROM sales"
    )

    total_sales = cursor2.fetchone()[0]

    return render_template(
        'sales.html',
        sales=data,
        total_sales=total_sales
    )


@app.route('/add_sale', methods=['POST'])
def add_sale():

    try:

        customer_name = request.form['customer_name']
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        total = request.form['total']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "INSERT INTO sales(customer_name, product_name, quantity, total) VALUES (?, ?, ?, ?)",
            (customer_name, product_name, quantity, total)
        )

        conn.execute(
            "UPDATE products SET quantity = quantity - ? WHERE product_name=?",
            (quantity, product_name)
        )

        conn.commit()

        return render_template(
            'success.html',
            message="Sale Added Successfully"
        )

    except:

        return "Error Adding Sale"


@app.route('/delete_sale/<int:id>')
def delete_sale(id):

    conn = sqlite3.connect('database.db')

    conn.execute(
        "DELETE FROM sales WHERE id=?",
        (id,)
    )

    conn.commit()

    return render_template(
        'success.html',
        message="Sale Deleted Successfully"
    )


# =========================
# USER MODULE
# =========================

@app.route('/users')
def users():

    conn = sqlite3.connect('database.db')

    cursor = conn.execute(
        "SELECT * FROM users"
    )

    data = cursor.fetchall()

    return render_template(
        'users.html',
        users=data
    )


@app.route('/add_user', methods=['POST'])
def add_user():

    try:

        username = request.form['username']
        email = request.form['email']

        conn = sqlite3.connect('database.db')

        conn.execute(
            "INSERT INTO users(username, email) VALUES(?, ?)",
            (username, email)
        )

        conn.commit()

        return redirect('/users')

    except:

        return "Error Adding User"


# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(debug=True)