import pandas as pd
from itertools import combinations

from roster import CANONICAL_PLAYERS


# TODO
# Form
# Player Rank
# Last MOTM
# Last GOTG
# Last Goals
# Last Rating
# Goals per GOTG
# Order columns
# Put played LT3 in separate table

def convert_to_player_table(df):
    df = df.copy()

    total_goals = df["Goals"].sum()

    # Ensure Result column is uppercase
    df["Result"] = df["Result"].str.upper()

    # Create outcome columns
    df["Win"] = (df["Result"] == "W").astype(int)
    df["Draw"] = (df["Result"] == "D").astype(int)
    df["Loss"] = (df["Result"] == "L").astype(int)

    # Points system: 3 for Win, 1 for Draw
    df["Points"] = df["Win"] * 3 + df["Draw"]

    # Convert MOTM to numeric (if True/False or 1/0)
    df["MOTM"] = df["MOTM"].astype(int)
    df["GOTG"] = df["GOTG"].astype(int)

    df["Team_GD"] = df["Team GF"].astype(int) - df["Team GA"].astype(int)

    # Create player summary table
    player_table = df.groupby("Name").agg(
        Played=("Name", "count"),
        Wins=("Win", "sum"),
        Draws=("Draw", "sum"),
        Losses=("Loss", "sum"),
        Goals=("Goals", "sum"),
        MOTM=("MOTM", "sum"),
        GOTG=("GOTG", "sum"),
        Points=("Points", "sum"),
        Avg_Rating=("Rating", "mean"),
        Team_GF=("Team GF", "sum"),
        Team_GA=("Team GA", "sum"),
        Team_GD=("Team_GD", "sum"),
    ).reset_index()

    player_table["Form"] = player_table["Name"].map(build_player_form(df))

    # % of total goals

    player_table['Win %'] = player_table['Wins'] / player_table['Played']
    player_table['GPG'] = player_table['Goals'] / player_table['Played']
    player_table['% of team goals'] = player_table['Goals'] / player_table['Team_GF']
    player_table['% of total goals'] = player_table['Goals'] / total_goals
    player_table['Ave TGF'] = player_table['Team_GF'] / player_table['Played']
    player_table['Ave TGA'] = player_table['Team_GA'] / player_table['Played']
    player_table['Ave TGD'] = player_table['Team_GD'] / player_table['Played']
    player_table['Ave MOTM'] = player_table['MOTM'] / player_table['Played']
    player_table['Ave GOTG'] = player_table['GOTG'] / player_table['Played']

    # Sort like a proper league table
    player_table = player_table.sort_values(
        by=["Points", "Team_GD", "Goals"],
        ascending=False
    ).reset_index(drop=True)

    player_table = player_table[
        ['Name', 'Form', 'Avg_Rating', 'Played', 'Wins', 'Draws', 'Losses', 'Points', 'Win %', 'Goals', 'GPG',
         '% of team goals', '% of total goals', 'Team_GF', 'Team_GA', 'Team_GD', 'Ave TGF', 'Ave TGA', 'Ave TGD',
         'MOTM', 'Ave MOTM', 'GOTG', 'Ave GOTG']]

    # Pos.,,Player,Form,Rating,Player Rank, Last match MOTM,Last match GOTG

    return player_table


def calculate_form(df):
    pass


def analytics_filter(df, remove_part_timers=False):
    if not remove_part_timers:
        return df.copy()

    appearances = df.groupby("Name").size()
    eligible_players = appearances[appearances >= 3].index
    return df[(df["Name"].isin(eligible_players)) & (df["Name"] != "Ringer")].copy()


def ordered_match_dates(df):
    return sorted(df["Date"].dropna().unique().tolist())


def build_player_form(df, last_n=5):
    ordered_dates = ordered_match_dates(df)
    player_results = (
        df.sort_values(["Date", "Name"])
        .drop_duplicates(subset=["Name", "Date"], keep="last")
        .set_index(["Name", "Date"])["Result"]
        .to_dict()
    )

    form_map = {}
    for player in sorted(df["Name"].dropna().unique()):
        recent_results = [
            player_results.get((player, match_date), "-")
            for match_date in ordered_dates[-last_n:]
        ]
        form_map[player] = "".join(recent_results)
    return form_map


def last_game_stats(df):
    latest_date = df["Date"].max()
    return df[df["Date"] == latest_date][["Name", "Team", "Goals", "MOTM", "GOTG", "Rating"]]


def combination_league(df, x):
    """
    Create a league table for all combinations of x players across all matches they played together.

    Args:
        df (pd.DataFrame): Player game data.
        x (int): Number of players per combination.

    Returns:
        pd.DataFrame: Aggregated stats per player combination.
    """
    # Drop ringer
    df = df[df["Name"] != "Ringer"]

    # Store aggregated records
    combo_stats = {}

    # Group by match
    match_groups = df.groupby(['Team', 'Date'])

    for (team, date), group in match_groups:
        players = group['Name'].tolist()
        # Generate all combinations of size x in this match
        for combo in combinations(sorted(players), x):
            combo_key = tuple(combo)  # Use tuple as dict key
            if combo_key not in combo_stats:
                combo_stats[combo_key] = {
                    'Played': 0, 'Wins': 0, 'Draws': 0, 'Losses': 0,
                    'Goals': 0, 'MOTM': 0, 'GOTG': 0, 'Avg Rating': 0,
                    'Team GF': 0, 'Team GA': 0
                }

            combo_stats[combo_key]['Played'] += 1
            result = group['Result'].iloc[0]
            if result == 'W':
                combo_stats[combo_key]['Wins'] += 1
            elif result == 'L':
                combo_stats[combo_key]['Losses'] += 1
            else:
                combo_stats[combo_key]['Draws'] += 1

            combo_stats[combo_key]['Goals'] += group[group['Name'].isin(combo)]['Goals'].sum()
            combo_stats[combo_key]['MOTM'] += group[group['Name'].isin(combo)]['MOTM'].sum()
            combo_stats[combo_key]['GOTG'] += group[group['Name'].isin(combo)]['GOTG'].sum()
            combo_stats[combo_key]['Avg Rating'] += group[group['Name'].isin(combo)]['Rating'].mean()

            combo_stats[combo_key]['Team GF'] += group[group['Name'].isin(combo)]['Team GF'].sum()
            combo_stats[combo_key]['Team GA'] += group[group['Name'].isin(combo)]['Team GA'].sum()
            # combo_stats[combo_key]['Team GD'] += group[group['Name'].isin(combo)]['Team GD'].sum()

            # % of team and total goals

    # Convert to DataFrame
    league_table = []
    for combo, stats in combo_stats.items():
        # Average rating across matches
        stats['Avg_Rating'] = stats['Avg Rating'] / stats['Played']
        stats['Points'] = stats['Wins'] * 3 + stats['Draws']
        stats['Team GD'] = stats['Team GF'] - stats['Team GA']
        stats['Win %'] = stats['Wins'] / stats['Played']
        stats['GPG'] = stats['Goals'] / stats['Played']
        league_table.append({'Combination': combo, **stats})

    return pd.DataFrame(league_table).sort_values(by='Wins', ascending=False)


def generate_pair_records(df, roster=None):
    roster = roster or CANONICAL_PLAYERS
    combo_stats = {
        tuple(sorted(combo)): {"played": 0, "wins": 0}
        for combo in combinations(sorted(roster), 2)
    }

    grouped = df[df["Name"].isin(roster)].groupby(["Team", "Date"])
    for (_, _), group in grouped:
        players = sorted(group["Name"].unique().tolist())
        result = str(group["Result"].iloc[0]).upper()

        for combo in combinations(players, 2):
            stats = combo_stats[tuple(sorted(combo))]
            stats["played"] += 1
            if result == "W":
                stats["wins"] += 1

    records = {
        "never_played": [],
        "never_won": [],
        "perfect_record": [],
    }

    for combo, stats in combo_stats.items():
        if stats["played"] == 0:
            records["never_played"].append(combo)
        elif stats["wins"] == 0:
            records["never_won"].append(combo)
        elif stats["wins"] == stats["played"]:
            records["perfect_record"].append(combo)

    return records
