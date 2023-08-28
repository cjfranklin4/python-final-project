#!/usr/bin/env python3
import json
import sqlite3
import requests
import random

# Define the base URL
POKE_URL = "https://pokeapi.co/api/v2/pokemon"

BERRIES_URL = "https://pokeapi.co/api/v2/berry"

poke_id = []
berry_id = []
poke_array = []
berries = []

# search for pokemon
def pokelookup():
    # add 4 random ints to poke_id for the API calls
    for id in range(4):
        poke_id.append(random.randint(1, 900))
    #print(poke_id)


    # call the pokemon API for 4 pokemon
    for poke in poke_id:
        try:
            api = f"{POKE_URL}/{poke}"
            resp = requests.get(api)
            #print(api)
            data = resp.json()

            name = data["name"]
            image = data["sprites"]["front_shiny"]
            weight = data["weight"]
            types = data["types"]

            poke_array.append({
                'name': name,
                'image': image,
                'weight': weight,
                'types': types
            })


        except:
            return False

    #print(poke_array)

# search for berries
def berrylookup():
    # add 4 random ints to poke_id for the API calls
    for id in range(4):
        berry_id.append(random.randint(1, 64))


    # call the pokemon API for 4 pokemon
    for berry in berry_id:
        try:
            api = f"{BERRIES_URL}/{berry}"
            resp = requests.get(api)
            #print(api)
            data = resp.json()

            name = data["name"]
            flavor = data["flavors"]

            berries.append({
                'name': name,
                'flavor': flavor
            })


        except:
            return False

    #print("berry array", berries)

def organize_data():
    for poke in poke_array:
        poke["types_final"] = []
        for poke_type in poke["types"]:
            poketype = poke_type["type"]["name"]

            #add type to dictionary
            poke["types_final"].append(poketype)
    #print(poke_array)


    for berry in berries:
        berry["flavor_final"] = []
        for berry_flav in berry["flavor"]:
            if berry_flav['potency'] > 0:
                #print(berry_flav['flavor']['name'])
                flavor = berry_flav['flavor']['name']
                berry["flavor_final"].append(flavor)

def poke_database(datatotrack):
    conn = sqlite3.connect('pokemon.db')
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS POKEMON (ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, IMAGE TEXT NOT NULL, WEIGHT INT NOT NULL, TYPE TEXT NOT NULL);''')

        # loop through the list of movies that was passed in
        for data in datatotrack:
            print("I WORK IN DATA LOOP")
            print('data',data)
            # in the line below, the ? are examples of "bind vars"
            # this is best practice, and prevents sql injection attacks
            # never ever use f-strings or concatenate (+) to build your executions
            conn.execute("INSERT INTO POKEMON (NAME, IMAGE, WEIGHT, TYPE) VALUES (?,?,?,?)",(data.get("name"), data.get("image"), data.get("weight"), data.get("type_final")))
            print("I WORK AFTER EXECUTE")
            conn.commit()

        print("Database operation done")
        conn.close()
        return True
    except:
        return False



def main():
    pokelookup()
    berrylookup()
    organize_data()
    poke_database(poke_array)
    print("I WORK IN MAIN")


if __name__ == "__main__":
    main()

