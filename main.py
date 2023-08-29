#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
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

@app.route('/shop')
def shopping():

    #GET REQUEST
    poke_array = get_pokemon()
    berries = get_berries()


    #NEED POST REQUEST SECTION
    """
        POST request when you click the "Add to cart button"
        MAX 3 items in cart, if more than 3 items, you get an alert/warning about cart being full

        a new database (cart.db) should be created that keeps track of the items being added or removed from your cart
    """

    return render_template('shop.html', poke_array=poke_array, berries=berries)



@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2225, debug=True)
