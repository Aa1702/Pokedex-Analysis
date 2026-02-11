import sqlite3
import pandas as pd
import seaborn
import matplotlib
import os

conn = sqlite3.connect("data/pokedex.db")
query = "SELECT * FROM pokemon"
df = pd.read_sql(query,conn)
conn.close()

# --- LET'S LOOK AT DATA ---
print("📊 HERE IS YOUR POKEMON DATA:")
print(df)

# --- SIMPLE ANALYSIS ---
# Let's find the strongest Pokemon (highest Attack)
strongest = df.loc[df['attack'].idxmax()]

print("\n💪 THE STRONGEST POKEMON IS:")
print(f"Name: {strongest['name'].title()}")
print(f"Attack: {strongest['attack']}")
print(f"Type: {strongest['type_1']}")
print(f"HP: {strongest['hp']}")
print(f"Defense: {strongest['defense']}")
print(f"Speed: {strongest['speed']}")

