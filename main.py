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
    con = sql.connect("pokemon.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from POKEMON")     
    
    pokemon = cur.fetchall() 
    #print("pokemon", pokemon)
    con.close()
    return pokemon

def get_berries():
    con = sql.connect("berries.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from BERRIES")     
    
    berries = cur.fetchall() 
    #print("berries", berries)
    con.close()
    return berries

def get_cart():
    con = sql.connect("cart.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from CART")     
    
    cart = cur.fetchall() 
    #print("berries", berries)
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
        with sql.connect("cart.db") as con:
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
                err = "Too many items in cart"
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
    conn = sql.connect('cart.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM CART WHERE ID = ?', (item_id,))
    conn.commit()
    conn.close()

    poke_array = get_pokemon()
    berries = get_berries()
    cart = get_cart()
    return redirect(url_for('shopping', poke_array=poke_array, berries=berries, cart=cart))

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


if __name__ == "__main__":
    con = sql.connect('cart.db')
    print("Opened database successfully")
    con.execute('CREATE TABLE IF NOT EXISTS CART (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, TABLE_NAME TEXT, ITEM_ID INT)')
    print("Table created successfully")
    con.close()

    app.run(host="0.0.0.0", port=2225, debug=True)
