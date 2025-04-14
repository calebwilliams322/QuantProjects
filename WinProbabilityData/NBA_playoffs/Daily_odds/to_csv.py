import os
import json
import pandas as pd
from datetime import datetime

# Set the directory where your JSON files are stored
directory = "."  # change this to your folder path

# List to store extracted records
records = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            # Each file is assumed to contain a JSON array of game dictionaries
            print('hello')
            game_data = json.load(f)
            print(f"File: {filename}, Type: {type(game_data)}, Length: {len(game_data) if isinstance(game_data, list) else 'N/A'}")
        
        # Iterate over each game record in the file
        for game in game_data:
            # Extract common game-level information
            game_id = game.get("GameId")
            season = game.get("Season")
            season_type = game.get("SeasonType")
            day = game.get("Day")
            game_datetime = game.get("DateTime")
            status = game.get("Status")
            away_team = game.get("AwayTeamName")
            home_team = game.get("HomeTeamName")
            
            # Process each odds snapshot in the "PregameOdds" list
            pregame_odds = game.get("PregameOdds", [])
            for odds in pregame_odds:
                record = {
                    "GameId": game_id,
                    "Season": season,
                    "SeasonType": season_type,
                    "Day": day,
                    "GameDateTime": game_datetime,
                    "Status": status,
                    "AwayTeamName": away_team,
                    "HomeTeamName": home_team,
                    "GameOddId": odds.get("GameOddId"),
                    "Sportsbook": odds.get("Sportsbook"),
                    "Created": odds.get("Created"),
                    "Updated": odds.get("Updated"),
                    "HomeMoneyLine": odds.get("HomeMoneyLine"),
                    "AwayMoneyLine": odds.get("AwayMoneyLine"),
                    "HomePointSpread": odds.get("HomePointSpread"),
                    "AwayPointSpread": odds.get("AwayPointSpread"),
                    "HomePointSpreadPayout": odds.get("HomePointSpreadPayout"),
                    "AwayPointSpreadPayout": odds.get("AwayPointSpreadPayout"),
                    "OverUnder": odds.get("OverUnder"),
                    "OverPayout": odds.get("OverPayout"),
                    "UnderPayout": odds.get("UnderPayout"),
                    "SportsbookId": odds.get("SportsbookId"),
                    "OddType": odds.get("OddType"),
                    "SportsbookUrl": odds.get("SportsbookUrl")
                }
                records.append(record)

# Convert list of records into a Pandas DataFrame
df = pd.DataFrame(records)
print(records)
print(df.head())

# Convert timestamp fields to datetime objects for easier sorting and analysis
df["Created"] = pd.to_datetime(df["Created"])
df["Updated"] = pd.to_datetime(df["Updated"])
df["Day"] = pd.to_datetime(df["Day"])
df["GameDateTime"] = pd.to_datetime(df["GameDateTime"])

# Sort the DataFrame by GameId and the Created timestamp to get a proper time series for each game
df = df.sort_values(by=["GameId", "Created"])

# Save the aggregated data to a CSV file
output_csv = "aggregated_pregame_odds.csv"
df.to_csv(output_csv, index=False)
print(f"Aggregated data saved to {output_csv}")
