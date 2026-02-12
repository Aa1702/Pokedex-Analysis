import requests
import sqlite3
import os

# --- SETUP DATABASE ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/pokedex.db")
cursor = conn.cursor()

# We need to drop the old table to add the new 'sprite_url' column cleanly
cursor.execute("DROP TABLE IF EXISTS pokemon")

cursor.execute("""
CREATE TABLE pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type_1 TEXT,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    speed INTEGER,
    cry_url TEXT,
    sprite_url TEXT  -- << NEW COLUMN FOR IMAGES
)
""")
conn.commit()

# --- FETCH DATA ---
def fetch_pokemon(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            real_name = data['name']
            stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
            cry_url = data['cries']['latest']
            type_1 = data['types'][0]['type']['name']
            # GRAB THE IMAGE URL
            sprite_url = data['sprites']['front_default']

            print(f"⚡ Catching #{data['id']} {real_name}...")

            cursor.execute("""
                INSERT INTO pokemon (id, name, type_1, hp, attack, defense, speed, cry_url, sprite_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (data['id'], real_name, type_1, stats['hp'], stats['attack'], stats['defense'], stats['speed'], cry_url, sprite_url))
            
            conn.commit()
        else:
            print(f"❌ Error finding ID {pokemon_id}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

print("🚀 STARTING COLLECTION (Fetching Images)...")
# Let's get the first 151 (Gen 1) so you have plenty of data
for i in range(1, 152):
    fetch_pokemon(i)

print("\n✨ Database Updated! Now contains Images.")
conn.close()