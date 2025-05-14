import json
import requests

# INITALIZATION

# Fetches the map of abilities
ability_ids_url = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/ability_ids.json"
abilities_url = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/abilities.json"

ability_ids = requests.get(ability_ids_url).json()
abilities = requests.get(abilities_url).json()

# hero mapping fetching
hero_ids_url = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json"
heroes_url = "https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json"

# Load JSONs
hero_ids = requests.get(hero_ids_url).json()
heroes = requests.get(heroes_url).json()

GAME_MODES = {
    1: "All Pick",
    2: "Captains Mode",
    3: "Random Draft",
    4: "Single Draft",
    18: "Ability Draft",
    22: "Ranked All Pick",
    23: "Turbo"
}
    
def fetch_match(match_id = 8291337212):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        match_data = response.json()
        print(f"Match data for {match_id} has been successfully fetched!")
        # print("Match ID:", match_data['match_id'])
        # print("Duration (seconds):", match_data['duration'])
        # print("Radiant Win:", match_data['radiant_win'])
        # print("Radiant Score:", match_data['radiant_score'])
        # print("Dire Score:", match_data['dire_score'])
        # print("First Blood Time:", match_data['first_blood_time'])
    else:
        print("Failed to fetch match data. Status code:", response.status_code)
    return match_data


def get_ability_name_by_id(ability_id):
    ability_key = ability_ids.get(str(ability_id))
    if not ability_key:
        return f"Unknown ability ID: {ability_id}"
    
    ability_data = abilities.get(ability_key)
    if not ability_data:
        return f"Ability key '{ability_key}' not found in abilities.json"
    
    return str(ability_id) + ": " +ability_data.get('dname', ability_key)


def get_hero_name_by_id(hero_id):
    hero_id_str = str(hero_id)
    key = hero_ids.get(hero_id_str)
    return str(hero_id) + ": " + key['localized_name']



def get_player_profile_info(account_id, game_mode=18, match_limit=20):
    base_url = f"https://api.opendota.com/api/players/{account_id}"
    result = {"account_id": account_id, "game_mode_id": game_mode, "game_mode": GAME_MODES.get(game_mode, "Unknown")}

    try:
        
        # 1. Profile data: rank, behavior score
        player_data = requests.get(base_url).json()
        result["personaname"] = player_data.get("personaname", "Unknown")
        result["rank_tier"] = player_data.get("rank_tier", "Unknown")
        result["behavior_score"] = player_data.get("behavior_score", "Unknown")

        # 2. Win/loss all-time for this mode
        wl_data = requests.get(f"{base_url}/wl?game_mode={game_mode}").json()
        wins = wl_data.get("win", 0)
        losses = wl_data.get("lose", 0)
        result["wins"] = wins
        result["losses"] = losses
        total = wins + losses
        result["overall_winrate"] = f"{round(wins / total * 100, 2)}%" if total > 0 else "N/A"

        # 3. Last N matches winrate
        match_data = requests.get(f"{base_url}/matches?limit={match_limit}&game_mode={game_mode}").json()
        recent_wins = sum(
            1 for match in match_data
            if ("radiant_win" in match and
                ((match["player_slot"] < 128 and match["radiant_win"]) or
                 (match["player_slot"] >= 128 and not match["radiant_win"])))
        )
        result["last_{}_winrate".format(match_limit)] = (
            f"{round(recent_wins / len(match_data) * 100, 2)}%" if match_data else "N/A"
        )

    except Exception as e:
        result["error"] = str(e)

    return result


def check_ability_upgrades(ability_id):
    
    
    ability_key = ability_ids.get(str(ability_id))
    if not ability_key:
        return f"Unknown ability ID: {ability_id}"
    
    ability_data = abilities.get(ability_key)
    if not ability_data:
        return f"Ability key '{ability_key}' not found in abilities.json"
    
    result = {}
    
    # --- SHARD
    shard_grants = ability_data.get("shard_grants")
    if shard_grants:
        result["has_shard_upgrade"] = True
        result["shard_desc"] = shard_grants if isinstance(shard_grants, str) else None

    # --- SCEPTER
    scepter_grants = ability_data.get("scepter_grants")
    if scepter_grants:
        result["has_scepter_upgrade"] = True
        result["scepter_desc"] = scepter_grants if isinstance(scepter_grants, str) else None
    return result

