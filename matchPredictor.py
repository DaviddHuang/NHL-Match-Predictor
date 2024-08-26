import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score

def rolling_averages(group, cols, new_cols):
    group = group.sort_values("Date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

matches = pd.read_csv("matches.csv", index_col=0)
matches["Date"] = pd.to_datetime(matches["Date"])
matches["Venue_code"] = matches["Venue"].astype("category").cat.codes
matches["Opp_code"] = matches["Opponent"].astype("category").cat.codes
matches["Day_code"] = matches["Date"].dt.dayofweek
matches["Target"] = (matches["Result"] == "W").astype("int")

cols = ["GF", "GA", "S", "PIM", "PPG", "PPO", "SHG", "CF", "CA", "CF%", "FF", "FA", "FF%", "FOW", "FOL", "FO%", "oZS%", "PDO"]
new_cols = [f"{c}_rolling" for c in cols]
matches_rolling = matches.groupby("Team").apply(lambda x: rolling_averages(x, cols, new_cols))
matches_rolling = matches_rolling.droplevel("Team")
matches_rolling.index = range(matches_rolling.shape[0])

def make_predictions(data, predictors, target_col):
    train = data[data["Date"] < '2024-01-25']
    test = data[data["Date"] >= '2024-01-25']
    rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
    rf.fit(train[predictors], train[target_col])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test[target_col], predicted=preds), index=test.index)
    precision = precision_score(test[target_col], preds)
    return combined, precision

predictors = ["Venue_code", "Opp_code", "Day_code"] + new_cols
combined, precision = make_predictions(matches_rolling, predictors, "Target")
combined = combined.merge(matches_rolling[["Date", "Team", "Opponent", "Result"]], left_index=True, right_index=True)

class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {
    "ANA": "Anaheim Ducks",
    "ARI": "Arizona Coyotes",
    "BOS": "Boston Bruins",
    "BUF": "Buffalo Sabres",
    "CAR": "Carolina Hurricanes",
    "CBJ": "Columbus Blue Jackets",
    "CGY": "Calgary Flames",
    "CHI": "Chicago Blackhawks",
    "COL": "Colorado Avalanche",
    "DAL": "Dallas Stars",
    "DET": "Detroit Red Wings",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MTL": "Montreal Canadiens",
    "NJD": "New Jersey Devils",
    "NSH": "Nashville Predators",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins",
    "SJS": "San Jose Sharks",
    "SEA": "Seattle Kraken",
    "STL": "St. Louis Blues",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets",
    "WSH": "Washington Capitals"
}

mapping = MissingDict(**map_values)
combined["New_team"] = combined["Team"].map(mapping)
merged = combined.merge(combined, left_on=["Date", "New_team"], right_on=["Date", "Opponent"])
print(merged[(merged["predicted_x"] == 1) & (merged["predicted_y"] == 0)]["actual_x"].value_counts())
