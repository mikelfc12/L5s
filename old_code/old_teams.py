



new_team = ["Callum Goodyear", "Jamie Dobbs", "Steven Robinso", "Jacob Stokes", "Rory Scullin"]
is_bad, team_name = is_team_previously_contained(new_team, previous_teams)
print("X")
if is_bad:
    print(f"New team is a subset of previous team {team_name}")
else:
    print("New team is valid")
new_team = ["Michael Dixon", "Daniel Hirst", "James King", "Mark McGlinchey", "Ringer"]
is_bad, team_name = is_team_previously_contained(new_team, previous_teams)
print("XX")
if is_bad:
    print(f"New team is a subset of previous team {team_name}")
else:
    print("New team is valid")


def check_team_overlap(teams):
    team_items = list(teams.items())

    for i in range(len(team_items)):
        name1, team1 = team_items[i]
        set1 = set(player for player in team1 if player.strip())

        for j in range(i + 1, len(team_items)):
            name2, team2 = team_items[j]
            set2 = set(player for player in team2 if player.strip())

            if set1.issubset(set2):
                print(f"{name1} is fully contained within {name2}")

            elif set2.issubset(set1):
                print(f"{name2} is fully contained within {name1}")

            else:
                print(f"{name1} is not fully contained in {name2}")


print("XXX")
check_team_overlap(previous_teams)
