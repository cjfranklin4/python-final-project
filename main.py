#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
import sqlite3 as sql

#database helper functions
#Get items from the database helper functions
def get_pokemon():
    con = sql.connect("/data/inventory.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from POKEMON")     
    
    pokemon = cur.fetchall() 
    con.close()
    return pokemon

def get_berries():
    con = sql.connect("/data/inventory.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from BERRIES")     
    
    berries = cur.fetchall() 
    con.close()
    return berries

def get_cart():
    con = sql.connect("/data/cart.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from CART")     
    
    cart = cur.fetchall() 
    con.close()
    return cart

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")

@app.route('/shop')
def shopping():
    poke_array = get_pokemon()
    berries = get_berries()
    cart = get_cart()
    return render_template('shop.html', poke_array=poke_array, berries=berries, cart=cart)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    #if length of cart is less than 3 continue, else return an error alert/page

    #NO DOUBLES IN CART (maybe add later)
    try: 
        # connect to sqliteDB
        with sql.connect("/data/cart.db") as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM CART;')
            cart_len = len(cur.fetchall())
            #print(cart_len)

            if cart_len <= 2:
                item_id=request.form.get("item_id")
                item_type=request.form.get("item_type")
                item_name=request.form.get("item_name")

                cur.execute("INSERT INTO CART (NAME, TABLE_NAME, ITEM_ID) VALUES (?,?,?)",(item_name, item_type, item_id) )
                con.commit()
                msg = "Record successfully added"
            else:
                print("TOO MANY ITEMS IN CART")
                msg = "error in insert operation"
    except:
        con.rollback() 
        msg = "error in insert operation"

    finally:
        con.close()
        poke_array = get_pokemon()
        berries = get_berries()
        cart = get_cart()
        return redirect(url_for('shopping', poke_array=poke_array, berries=berries, cart=cart))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    conn = sql.connect('/data/cart.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM CART WHERE ID = ?', (item_id,))
    conn.commit()
    conn.close()

    poke_array = get_pokemon()
    berries = get_berries()
    cart = get_cart()
    return redirect(url_for('shopping', poke_array=poke_array, berries=berries, cart=cart))

@app.route("/checkout", methods = ["POST","GET"])
def checkout():
    if request.method == "POST":
        return redirect(url_for('Thankyou'))

    elif request.method == "GET":
        cart = get_cart()
        return render_template("checkout.html", cart=cart)

@app.route("/Thankyou")
def Thankyou():
    cart = get_cart()

    conn = sql.connect('/data/cart.db')
    cursor = conn.cursor()

    cursor.execute('SELECT NAME, TABLE_NAME, ITEM_ID FROM CART')
    rows = cursor.fetchall()

    inventory = []
    for row in rows:
        item = {
            'name': row[0],
            'table_name': row[1],
            'item_id': row[2]
        }
        inventory.append(item)
    
    cursor.execute('DELETE FROM CART')
    conn.commit()
    conn.close()

    receipt = []
    for item in inventory:
        item_id=item['item_id']
        table_name=item['table_name']

        conn = sql.connect('/data/inventory.db')
        cursor = conn.cursor()

        if table_name == 'POKEMON':
            query = 'SELECT * FROM POKEMON WHERE ID = ?'
        else:
            query = 'SELECT * FROM BERRIES WHERE ID = ?'

        cursor.execute(query, (item_id,))
        rows = cursor.fetchone()
        print(rows)
        receipt.append(rows)
        conn.close()

    return render_template("Thankyou.html", receipt=receipt)

if __name__ == "__main__":
    con = sql.connect('/data/cart.db')
    print("Opened database successfully")
    con.execute('CREATE TABLE IF NOT EXISTS CART (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, TABLE_NAME TEXT, ITEM_ID INT)')
    print("Table created successfully")
    con.close()

    app.run(host="0.0.0.0", port=2225, debug=True)
