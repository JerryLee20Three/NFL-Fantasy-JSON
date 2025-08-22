import requests
import json
import subprocess

# ---------- CONFIGURATION ----------
LEAGUE_ID = "YOUR_LEAGUE_ID"       # replace with your ESPN league ID
SEASON = 2025
BASE_URL = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"

COOKIES = {
    'SWID': '{YOUR_SWID}',
    'espn_s2': 'YOUR_ESPN_S2'
}

POSITION_MAP = {1:"QB", 2:"RB", 3:"WR", 4:"TE", 5:"K", 16:"DEF"}

def get_headshot_url(name):
    return f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"

# ---------- FETCH DATA ----------
response = requests.get(BASE_URL, cookies=COOKIES)
data = response.json()

players_list = []

for team in data.get("teams", []):
    for entry in team.get("roster", {}).get("entries", []):
        player = entry.get("playerPoolEntry", {}).get("player", {})
        if not player:
            continue
        pos_id = player.get("defaultPositionId")
        position = POSITION_MAP.get(pos_id)
        if position not in ["QB","RB","WR","TE","K","DEF"]:
            continue
        
        lineup_slot = entry.get("lineupSlotId", 20)
        status = "starter" if lineup_slot < 16 else "bench"

        players_list.append({
            "playerId": str(player.get("id")),
            "displayName": player.get("fullName"),
            "team": player.get("proTeamId"),
            "position": position,
            "flex": position in ["RB","WR","TE"],
            "headshotUrl": get_headshot_url(player.get("fullName")),
            "status": status
        })

# ---------- SAVE JSON ----------
json_file = "espn_fantasy_players.json"
with open(json_file, "w") as f:
    json.dump(players_list, f, indent=4)

print(f"JSON file created: {json_file}")

# ---------- AUTOMATIC GITHUB PUSH ----------
# Make sure your repo is already cloned locally and this script is inside the repo folder
subprocess.run(["git", "add", json_file])
subprocess.run(["git", "commit", "-m", "Daily update of ESPN fantasy players"])  
subprocess.run(["git", "push"])