import random


def check_pairs(team, pairs):
    conflicts = []
    for p1, p2 in pairs:
        if p1 in team and p2 in team:
            conflicts.append((p1, p2))
    return conflicts


def generate_teams(pot_1, base_team_A, base_team_B, previous_teams):
    while True:
        team_A = base_team_A.copy()
        team_B = base_team_B.copy()

        # ---- POT 1 ----
        pot1_selected_for_A = random.sample(pot_1, 2)
        pot1_remaining_for_B = [p for p in pot_1 if p not in pot1_selected_for_A]

        team_A.extend(pot1_selected_for_A)
        team_B.extend(pot1_remaining_for_B)

        contained_A, _ = is_team_previously_contained(team_A, previous_teams)
        contained_B, _ = is_team_previously_contained(team_B, previous_teams)

        # ✅ Check both teams
        if not contained_A and not contained_B:
            return team_A, team_B


def is_team_previously_contained(new_team, previous_teams):
    new_set = set(player for player in new_team if player.strip())

    for team_name, old_team in previous_teams.items():
        old_set = set(player for player in old_team if player.strip())

        # Check if entire new team is inside old team
        if new_set.issubset(old_set):
            return True, team_name

    return False, None
