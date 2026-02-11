import requests
import sqlite3 
import os

conn = sqlite3.connect("data/pokedex.db")
cursor = conn.cursor()

cursor.execute("""  
CREATE TABLE IF NOT EXISTS pokemon(
id INTEGER PRIMARY KEY,
name TEXT,
type_1 TEXT,
hp INTEGER,
attack INTEGER,
defense INTEGER,
speed INTEGER,
cry_url TEXT
)    
""")
conn.commit()

# --- FETCH DATA ---
def fetch_pokemon(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extracting the "Powers" (Stats)
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        
        # Extracting the "Voice" (Cry) - New feature!
        # The API usually provides an OGG file for the latest cry
        cry_url = data['cries']['latest']
        
        # Extracting Type
        type_1 = data['types'][0]['type']['name']

        print(f"⚡ Catching {pokemon_name}...")
        print(f"   - Type: {type_1}")
        print(f"   - Attack: {stats['attack']}")
        print(f"   - Voice: {cry_url}")

        # --- SQL LESSON: DML (Data Manipulation Language) ---
        # We use INSERT to add data.
        cursor.execute("""
            INSERT OR REPLACE INTO pokemon (id, name, type_1, hp, attack, defense, speed, cry_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['id'], pokemon_name, type_1, stats['hp'], stats['attack'], stats['defense'], stats['speed'], cry_url))
        
        conn.commit()
    else:
        print(f"❌ Could not find {pokemon_name}")

# --- LET'S START ---
fetch_pokemon("pikachu")
fetch_pokemon("eevee")
fetch_pokemon("charmander")
fetch_pokemon("jigglypuff") # The singer!

print("\n✨ All Pokémon caught and saved to SQL database!")
conn.close()