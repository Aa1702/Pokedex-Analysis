import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# --- BLOCK 1: DATA LOADING ---
conn = sqlite3.connect("data/pokedex.db")
df = pd.read_sql("SELECT * FROM pokemon", conn)
conn.close()

# --- BLOCK 2: STYLE SETTINGS ---
# Using a standard clean font that everyone has
plt.rcParams['font.family'] = 'sans-serif'

# The Spring Palette (Warm & Visible)
spring_palette = ["#FFB7B2", "#FFDAC1", "#FFE15D", "#C7E9B0", "#A8E6CF", "#B3E5BE", "#99E1E5", "#F8C4B4", "#E5EBB2", "#FFD8A8"]

def create_clean_spring_chart(metric, title):
    # Prepare Data
    top_10 = df.sort_values(by=metric, ascending=False).head(10).copy()
    top_10['name'] = top_10['name'].str.capitalize() # Capitalize names
    
    # Create figure with a warm "creamy" background
    plt.figure(figsize=(10, 6), facecolor='#FFF8F0')
    ax = plt.gca()
    ax.set_facecolor('#FFF8F0')

    # --- BLOCK 3: THE PAINTING ---
    sns.barplot(
        x=metric, 
        y="name", 
        data=top_10, 
        palette=spring_palette,
        edgecolor="white", # Sticker effect
        linewidth=2
    )

    # --- BLOCK 4: TEXT DECORATIONS (No Emojis!) ---
    # We use ~*~ to give it a whimsical, cute feel
    plt.title(f"~*~ {title} ~*~", fontsize=20, fontweight='bold', color="#6D8299", pad=20)
    plt.xlabel(metric.replace('_', ' ').capitalize(), fontsize=12, fontweight='bold', color="#889EAF")
    plt.ylabel("") 

    # Style the Y-axis labels
    plt.yticks(fontweight='bold', color="#555555")

    # Clean up the borders
    sns.despine(left=True, bottom=True)
    
    # Add soft grid lines
    plt.grid(axis='x', linestyle='--', alpha=0.3, color='#D8C4B6')

    print(f"Success! Painting the {title} chart...")
    plt.tight_layout()
    plt.show()

# --- BLOCK 5: GENERATE ---
create_clean_spring_chart("attack", "Strongest Buds of Gen 1")
create_clean_spring_chart("speed", "Zippy Spring Friends")
create_clean_spring_chart("defense", "Tough Little Sprouts")