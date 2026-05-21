import random


def check_pairs(team, pairs):
    conflicts = []
    for p1, p2 in pairs:
        if p1 in team and p2 in team:
            conflicts.append((p1, p2))
    return conflicts


def generate_teams(base_team_A, base_team_B, previous_teams, *pots):
    if not pots:
        raise ValueError("At least one pot must be provided")

    if len(pots) > 5:
        raise ValueError("A maximum of 5 pots is supported")

    max_attempts = 1000

    for _ in range(max_attempts):
        team_A = base_team_A.copy()
        team_B = base_team_B.copy()

        for pot in pots:
            mode, players = _normalise_pot(pot)

            if mode == "split":
                if len(players) % 2 != 0:
                    raise ValueError("Each split pot must contain an even number of players")

                players_for_a = random.sample(players, len(players) // 2)
                players_for_b = [player for player in players if player not in players_for_a]
                team_A.extend(players_for_a)
                team_B.extend(players_for_b)
                continue

            if mode == "keep":
                if len(team_A) < len(team_B):
                    team_A.extend(players)
                elif len(team_B) < len(team_A):
                    team_B.extend(players)
                elif random.choice([True, False]):
                    team_A.extend(players)
                else:
                    team_B.extend(players)
                continue

            raise ValueError(f"Unsupported pot mode: {mode}")

        contained_A, _ = is_team_previously_contained(team_A, previous_teams)
        contained_B, _ = is_team_previously_contained(team_B, previous_teams)

        if not contained_A and not contained_B:
            return team_A, team_B

    raise ValueError("Unable to generate a new team combination from the available pots")


def _normalise_pot(pot):
    if isinstance(pot, tuple):
        if len(pot) != 2:
            raise ValueError("Pot tuples must be in the format: (mode, players)")
        mode, players = pot
        return mode, list(players)

    return "split", list(pot)


def is_team_previously_contained(new_team, previous_teams):
    new_set = set(player for player in new_team if player.strip())

    for team_name, old_team in previous_teams.items():
        old_set = set(player for player in old_team if player.strip())

        # Only reject exact repeats of a previously drawn team.
        if len(new_set) == len(old_set) and new_set == old_set:
            return True, team_name

    return False, None
