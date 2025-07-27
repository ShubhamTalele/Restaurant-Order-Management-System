from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7744",
    database="restaurant"
)
cursor = db.cursor()

# my route
@app.route('/')
def landing():
    return render_template('landing.html')

#---this is for menu page
@app.route('/menu')
def menu():
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    return render_template('menu.html', menu=items)

#----this is for my create order

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        table_number = request.form['table_number']
        
      
        selected_items = []
        
      
        for item in items:
            item_id = item[0]  
            if request.form.get(f'item_{item_id}') and request.form.get(f'qty_{item_id}'): 
                qty = int(request.form[f'qty_{item_id}'])  
                if qty > 0:  
                    selected_items.append((item_id, qty))
        
        # if not selected_items:
        #     return "Please select at least one item and quantity.", 400

      
        cursor.execute("INSERT INTO orders (customer_name, table_number, total_amount) VALUES (%s, %s, %s)",
                       (customer_name, table_number, 0))
        db.commit()
        order_id = cursor.lastrowid  

       
        total_amount = 0
        for item_id, qty in selected_items:
            cursor.execute("SELECT price FROM menu_items WHERE item_id = %s", (item_id,))
            price = cursor.fetchone()[0]  
            total_amount += price * qty
            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                           (order_id, item_id, qty))  

        cursor.execute("UPDATE orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))
        db.commit()

        return redirect(url_for('view_orders'))  

    return render_template('create_order.html', menu=items)  

#----
@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
   
    cursor.execute("SELECT customer_name, table_number FROM orders WHERE order_id = %s", (order_id,))
    order = cursor.fetchone()


    cursor.execute("SELECT * FROM menu_items")
    menu = cursor.fetchall()

    cursor.execute("SELECT item_id, quantity FROM order_items WHERE order_id = %s", (order_id,))
    selected_items = dict(cursor.fetchall())

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        table_number = request.form['table_number']

        new_selected_items = {}
        for item in menu:
            item_id = item[0]
            qty = request.form.get(f'qty_{item_id}')
            if request.form.get(f'item_{item_id}') and qty:
                qty = int(qty)
                if qty > 0:
                    new_selected_items[item_id] = qty

        # if not new_selected_items:
        #     return "Please select at least one item with quantity.", 400

        cursor.execute("UPDATE orders SET customer_name=%s, table_number=%s WHERE order_id=%s",
                       (customer_name, table_number, order_id))

        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))

     
        total_amount = 0
        for item_id, qty in new_selected_items.items():
            cursor.execute("SELECT price FROM menu_items WHERE item_id = %s", (item_id,))
            price = cursor.fetchone()[0]
            total_amount += price * qty
            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                           (order_id, item_id, qty))

        cursor.execute("UPDATE orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))
        db.commit()

        return redirect(url_for('view_orders'))

    return render_template('edit_order.html', order_id=order_id, order=order, menu=menu, selected_items=selected_items)



@app.route('/view_orders')
def view_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return render_template('view_orders.html', orders=orders)

@app.route('/delete_order/<order_id>', methods=['POST'])
def delete_order(order_id):
    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    db.commit()
    return redirect(url_for('view_orders'))

@app.route('/generate_bill/<order_id>')
def generate_bill(order_id):
    cursor.execute("""
        SELECT orders.order_id, orders.customer_name, orders.table_number, orders.total_amount,
        GROUP_CONCAT(CONCAT(menu_items.item_name, ' x', order_items.quantity) SEPARATOR ', ') AS items
        FROM orders
        JOIN order_items ON orders.order_id = order_items.order_id
        JOIN menu_items ON order_items.item_id = menu_items.item_id
        WHERE orders.order_id = %s
        GROUP BY orders.order_id
    """, (order_id,))
    bill = cursor.fetchone()
    return render_template('generate_bill.html', bill=bill)

if __name__ == "__main__":
    app.run(debug=True)
