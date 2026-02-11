import os
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import seaborn as sns

# Block 1 GET THE DATA!!
# Connect to our box (database) and grab the data with Pandas

conn = sqlite3.connect("data/pokedex.db")
query = "SELECT * FROM pokemon"
df = pd.read_sql(query, conn)
conn.close()

# BLOCK 2: PREPARE THE DATA 
# Sort the Pokémon by 'attack' (strongest first)
# .head(10) means "Only give me the top 10 rows"

top_10 = df.sort_values(by = 'attack', ascending=False).head(10)

# BLOCK 3: SET THE VIBE (AESTHETICS) 
# This sets the background to a clean, cozy white grid

sns.set_theme(style = "whitegrid")
plt.figure(figsize= (10, 6))

# BLOCK 4: THE PAINTING (BAR CHART)
# x: How long the bar is (Attack Power)
# y: The label for the bar (Pokemon Name)
# palette="pastel": This makes the colors cute and soft! 🌸

sns.barplot(x = "attack", y = "name", data = top_10, palette = "pastel")

# BLOCK 5: THE FINISHING TOUCHES

plt.title("✨ Top 10 Strongest Pokémon (Gen 1) ✨", fontsize=16)
plt.xlabel("Attack Power", fontsize=12)
plt.ylabel("Pokemon Name", fontsize=12)

# This removes the ugly border box (makes it look modern)
sns.despine(left=True, bottom=True)

# BLOCK 6: REVEAL THE MASTERPIECE 
print("🎨 Painting your chart...")
plt.show()