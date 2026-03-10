import itertools
import pandas as pd


def create_even_teams(players, metric='both'):
    """
    players: list of dicts
    [
        {"name": "Player1", "rating": 7.5, "gpg": 0.6},
        ...
    ]
    """

    n = len(players)
    half = n // 2

    if n % 2 != 0:
        raise ValueError("Number of players must be even")

    best_diff = float("inf")
    best_split = None

    # Try all possible combinations of half the players
    for team1_indices in itertools.combinations(range(n), half):
        team1 = [players[i] for i in team1_indices]
        team2 = [players[i] for i in range(n) if i not in team1_indices]

        rating_diff = abs(sum(p["rating"] for p in team1) - sum(p["rating"] for p in team2))

        gpg_diff = abs(sum(p["gpg"] for p in team1) - sum(p["gpg"] for p in team2))

        if metric == 'rating':
            total_diff = rating_diff

        if metric == 'gpg':
            total_diff = gpg_diff

        if metric == 'both':
            total_diff = rating_diff + gpg_diff

        if total_diff < best_diff:
            best_diff = total_diff
            best_split = (team1, team2)

    return best_split


# Example usage
players = [
    {"name": "Steven Robinson", "rating": 4.63308784601521, "gpg": 2.85714285714286},
    {"name": "Jacob Stokes", "rating": 4.23664791339665, "gpg": 2.8},
    {"name": "Michael Dixon", "rating": 5.60949289152309, "gpg": 5.5},
    {"name": "Rory Scullin", "rating": 4.47886061954726, "gpg": 4},
    {"name": "Callum Goodyear", "rating": 4.86736535699885, "gpg": 4.85714285714286},
    {"name": "Mark McGlinchey", "rating": 3.94730087791277, "gpg": 2},
    {"name": "Daniel Hirst", "rating": 3.96243270487789, "gpg": 1.16666666666667},
    {"name": "Jamie Dobbs", "rating": 5.65686900804856, "gpg": 5.57142857142857},
    {"name": "James King", "rating": 5.66609170533891, "gpg": 6.16666666666667},
    {"name": "Ringer", "rating": 4.90263750318847, "gpg": 3},

]

for metric in ['rating', 'gpg', 'both']:
    team1, team2 = create_even_teams(players, metric)

    print("\n")
    print("Creating the most even teams based on", metric)

    print("TEAM 1")
    for p in team1:
        print(p["name"])
    print("Total Rating:", sum(p["rating"] for p in team1))
    print("Total GPG:", sum(p["gpg"] for p in team1))

    print("\nTEAM 2")
    for p in team2:
        print(p["name"])
    print("Total Rating:", sum(p["rating"] for p in team2))
    print("Total GPG:", sum(p["gpg"] for p in team2))
