#!/usr/bin/python3

from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from sqlite3 import sqlite

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")

@app.route("/shop")
def shopping():
    return render_template("shop.html")
with sql.connect(pokemon.db) as con():
    cur = con.cursor()
    cur.execute("SELECT * FROM POKEMON")

with sql.connect(berries.db) as con2():
    cur = con2.cursor()
    cur.execute("SELECT * FROM BERRIES")



@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

con.close()

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2224, debug=True)
