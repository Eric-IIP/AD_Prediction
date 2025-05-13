import requests

# goes match id here
match_id = 8291337212
url = f"https://api.opendota.com/api/matches/{match_id}"

response = requests.get(url)

if response.status_code == 200:
    match_data = response.json()
    print("Match ID:", match_data['match_id'])
    print("Duration (seconds):", match_data['duration'])
    print("Radiant Win:", match_data['radiant_win'])
    print("Radiant Score:", match_data['radiant_score'])
    print("Dire Score:", match_data['dire_score'])
    print("First Blood Time:", match_data['first_blood_time'])
else:
    print("Failed to fetch match data. Status code:", response.status_code)
