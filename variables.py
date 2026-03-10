# --- Player GIFs ---
player_images = {
    "Jacob Stokes": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKAbxsF4po4n8NRr893upXBUCyz3B2_h-ZzQ&s",
    "Daniel Hirst": "https://www.firmastella.com/wp-content/uploads/2024/11/hr-hirst.jpg",
    "Mark McGlinchey": "https://pbs.twimg.com/media/GOiFopxXYAA0vSy.jpg",
    "Kevin": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs_HFqpluDRv7K0jY-wrfPqSyz2lNFEUUI2w&s",
    "Jamie Dobbs": "https://upload.wikimedia.org/wikipedia/commons/3/38/Jamie_Oliver_%28cropped%29.jpg",
    "James King": "https://media.cnn.com/api/v1/images/stellar/prod/230508143040-01c-king-charles-official-portrait-0508.jpg?c=original",
    "Steven Robinson": "https://i.makeagif.com/media/6-26-2015/8zvaxF.gif",
    "Rory Scullin": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBmo64c-9oqlz3HgNQSqftgRzNrDVJrtP38A&s",
    "Callum Goodyear": "https://i.ytimg.com/vi/SfmVwWGIRKM/maxresdefault.jpg",
    "Michael Dixon": "https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p29708751_b_v13_ad.jpg",

    "Toby Munson": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnp7giyKeCdxXgwGiPxvn9RAdZxcPV2Hjgtg&s",
    "Callum Ringer": "Callum_Ringer.png",
    "John Bridgeman": "https://i.ytimg.com/vi/Uj5iPDcRiUg/maxresdefault.jpg",
    "Oliver Deverall": "https://cdn.apollo.audio/one/media/67ea/bef4/6652/c18e/45ef/7497/Olly-Murs.jpg?quality=80&format=jpg&crop=0,0,2540,4510&resize=crop"
}

player_stats = {
    "Jacob Stokes": "Match ball hoarder",
    "Oliver Deverall": "Fresh off his first win",
    "Callum Goodyear": "Sore knee who dis",
    "Mark McGlinchey": "Tonights the night",
    "Steven Robinson": "MOTM can he go b2b",
    "Daniel Hirst": "Suffering from the dreaded DOMs",
    "Jamie Dobbs": "1 of 2 players to record 3 wins on the bounce.",
    "Michael Dixon": "Happy to get off the losing train",
    "Rory Scullin": "Won, lost, won, lost, won, ......???",
    "James King": "Quad, feel, stronger, now, ooooh",
}

CARD_IMAGES = {
    "Jacob Stokes": "JS_card.png",
    "Michael Dixon": "MD_card.png",
    "Daniel Hirst": "DH_card.png",
    "Oliver Deverall": "OD_card.png",
    "Mark McGlinchey": "MM_card.png",
    "Rory Scullin": "RS_card.png",
    "Steven Robinson": "SR_card.png",
    "Jamie Dobbs": "JD_card.png",
    "Callum Goodyear": "CG_card.png",
    "James King": "JK_card.png"
}

never_played_pairs = [
    ("Toby Munson", "Callum Goodyear"),
]

never_won_pairs = [
    ("Mark McGlinchey", "Daniel Hirst"),
    ("Mark McGlinchey", "Callum Goodyear"),
    ("Mark McGlinchey", "Toby Munson"),
    ("Mark McGlinchey", "Oliver Deverall"),
    ("Mark McGlinchey", "Jamie Dobbs"),
    ("Mark McGlinchey", "Steven Robinson"),
    ("Toby Munson", "Oliver Deverall"),
    ("Toby Munson", "Michael Dixon"),
    ("Toby Munson", "James King"),
    ("Toby Munson", "Callum Goodyear"),
    ("Toby Munson", "Rory Scullin"),
    ("Toby Munson", "Steven Robinson"),
    ("Oliver Deverall", "Daniel Hirst"),
    ("Oliver Deverall", "Jacob Stokes"),
    ("Oliver Deverall", "James King"),
    ("Oliver Deverall", "Jamie Dobbs"),
    ("Steven Robinson", "Daniel Hirst"),
]

perfect_record_pairs = [
    ("Michael Dixon", "Jamie Dobbs"),
    ("Callum Goodyear", "Jacob Stokes"),
    ("Callum Goodyear", "James King"),
    ("Rory Scullin", "Daniel Hirst"),
    ("Rory Scullin", "Jacob Stokes"),
    ("Rory Scullin", "Jamie Dobbs"),
    ("Steven Robinson", "Jacob Stokes"),
]

previous_teams = {
    "A1": ["Michael Dixon", "Daniel Hirst", "Jacob Stokes", "James King", "Callum Goodyear", "Rory Scullin"],
    "B1": ["Toby Munson", "Oliver Deverall", "Mark McGlinchey", "Jamie Dobbs", "Steven Robinson"],
    "A2": ["Michael Dixon", "Daniel Hirst", "Neil Roberton", "Callum Goodyear", "Jamie Dobbs"],
    "B2": ["Toby Munson", "Oliver Deverall", "Mark McGlinchey", "James King", "Steven Robinson", "Rory Scullin"],
    "A3": ["Michael Dixon", "Daniel Hirst", "Oliver Deverall", "Jacob Stokes", "Toby Munson"],
    "B3": ["Jamie Dobbs", "Callum Goodyear", "James King", "Steven Robinson", "Rory Scullin"],
    "A4": ["Michael Dixon", "Callum Goodyear", "Mark McGlinchey", "Rory Scullin", "Steven Robinson"],
    "B4": ["Jamie Dobbs", "Toby Munson", "Daniel Hirst", "Jacob Stokes", "Ringer"],
    "A5": ["Oliver Deverall", "Callum Goodyear", "Steven Robinson", "Rory Scullin", "Michael Dixon"],
    "B5": ["Mark McGlinchey", "Daniel Hirst", "Jacob Stokes", "Jamie Dobbs", "James King"],
    "A6": ["Callum Goodyear", "Oliver Deverall", "Daniel Hirst", "Jamie Dobbs", "Steven Robinson"],
    "B6": ["Michael Dixon", "Jacob Stokes", "James King", "Mark McGlinchey", "Rory Scullin"],
    "A7": ["Callum Goodyear", "Ringer", "Ringer", "John Bridgman", "Rory Scullin"],
    "B7": ["Jamie Dobbs", "Steven Robinson", "James King", "Oliver Deverall", "Ringer"],
}
