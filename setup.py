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

    #print("pokemon array", poke_array)

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

    for berry in berries:
        berry["flavor_final"] = []
        for berry_flav in berry["flavor"]:
            if berry_flav['potency'] > 0:
                print(berry_flav['flavor']['name'])
                flavor = berry_flav['flavor']['name']
                berry["flavor_final"].append(flavor)





def main():
    pokelookup()
    berrylookup()
    organize_data()


if __name__ == "__main__":
    main()

