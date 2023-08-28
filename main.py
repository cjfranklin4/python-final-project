#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import make_response
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")

#Get items from the database
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

@app.route('/shop', methods = ["POST","GET"])
def shopping():
    poke_array = get_pokemon()
    berries = get_berries()
    cart = get_cart()
    if request.method == "GET":
        return render_template('shop.html', poke_array=poke_array, berries=berries, cart=cart)

    elif request.method == "POST":
        """
        POST request when you click the "Add to cart button"
        MAX 3 items in cart, if more than 3 items, you get an alert/warning about cart being full

        a new database (cart.db) should be created that keeps track of the items being added or removed from your cart
        """

        #if length of cart is less than 3 continue, else return an error alert/page

        #NO DOUBLES IN CART
        try: 
            # connect to sqliteDB
            with sql.connect("cart.db") as con:
                cur = con.cursor()
                cur.execute('SELECT * FROM CART;')
                cart_len = len(cur.fetchall())
                print(cart_len)

                if cart_len <= 2:
                    item_id=request.form.get("item_id")
                    item_type=request.form.get("item_type")
                    item_name=request.form.get("item_name")
                    

                    """ print(item_id, "THIS IS TH EITEM ID")
                    print(item_type, "THIS IS TH EITEM TYPE") """

                    cur.execute("INSERT INTO CART (NAME, TABLE_NAME, ID) VALUES (?,?,?)",(item_name, item_type, item_id) )
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
            return redirect(url_for('shopping', poke_array=poke_array, berries=berries, cart=cart, err=err))



@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


if __name__ == "__main__":
    con = sql.connect('cart.db')
    print("Opened database successfully")
    # ensure that the table students is ready to be written to
    con.execute('CREATE TABLE IF NOT EXISTS CART (NAME TEXT, TABLE_NAME TEXT, ID INT)')
    print("Table created successfully")
    con.close()

    app.run(host="0.0.0.0", port=2224, debug=True)
