import pandas as pd
import json

# nflfastR roster URL (current season)
roster_url = "https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/data/players.csv"

# Read CSV
players = pd.read_csv(roster_url)

# Keep only fantasy-eligible positions
fantasy_positions = ["QB", "RB", "WR", "TE", "K", "DEF"]
players = players[players['position'].isin(fantasy_positions)]

# Create JSON structure
players_list = []

for _, row in players.iterrows():
    players_list.append({
        "playerId": row["gsis_id"],  # unique identifier
        "displayName": row["full_name"],
        "team": row["team"],
        "position": row["position"],
        "flex": row["position"] in ["RB", "WR", "TE"],
        "headshotUrl": f"https://via.placeholder.com/150?text={row['full_name'].replace(' ', '+')}",
        "status": "active"
    })

# Export JSON
with open("nflfastR_players.json", "w") as f:
    json.dump(players_list, f, indent=4)

print("JSON file ready for Lovable!")