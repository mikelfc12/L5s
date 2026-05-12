CANONICAL_PLAYERS = [
    "Rory Scullin",
    "Steven Robinson",
    "Callum Goodyear",
    "Toby Munson",
    "Michael Dixon",
    "Oliver Deverall",
    "Daniel Hirst",
    "Jacob Stokes",
    "Jamie Dobbs",
    "James King",
    "Mark McGlinchey",
]

PLAYER_ALIASES = {
    "callum": "Callum Goodyear",
    "callum goodyear": "Callum Goodyear",
    "dan": "Daniel Hirst",
    "daniel hirst": "Daniel Hirst",
    "devs": "Oliver Deverall",
    "james k": "James King",
    "james king": "James King",
    "jamie": "Jamie Dobbs",
    "jamie dobbs": "Jamie Dobbs",
    "jacob stokes": "Jacob Stokes",
    "mark": "Mark McGlinchey",
    "mark mcglinchey": "Mark McGlinchey",
    "michael dixon": "Michael Dixon",
    "mike": "Michael Dixon",
    "oliver deverall": "Oliver Deverall",
    "rory": "Rory Scullin",
    "rory scullin": "Rory Scullin",
    "steven": "Steven Robinson",
    "steven robinson": "Steven Robinson",
    "stokes": "Jacob Stokes",
    "stokesy": "Jacob Stokes",
    "toby": "Toby Munson",
    "toby munson": "Toby Munson",
}


def normalize_player_name(player_name):
    raw_name = str(player_name or "").strip()
    if not raw_name:
        return ""

    alias_key = raw_name.casefold()
    return PLAYER_ALIASES.get(alias_key, raw_name)
