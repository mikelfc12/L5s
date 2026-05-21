# --- Player GIFs ---
player_images = {
    "Josh Ringer": "https://hips.hearstapps.com/hmg-prod/images/josh1-699819456da34.jpg?crop=1xw:1xh;center,top&resize=640:*",
    "Oliver Deverall": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-JVoIV9n0noftXRrYJAvSxfDT_vlWzSfPNg&s",
       
    "Jacob Stokes": "https://cdn.staticneo.com/w/twilight/JacobBlack.jpg",
    "Steven Robinson": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Steven_Seagal_at_Russia_Expo.jpg",
    "Callum Goodyear": "https://ichef.bbci.co.uk/ace/standard/1680/cpsprodpb/2ae4/live/eca39d10-85d1-11f0-961b-671d5baac859.jpg",
    "Jamie Dobbs": "https://e1.365dm.com/12/02/800x600/Jamie-O-Hara-Wolves_2720005.jpg?20120217102810",
    "Michael Dixon": "https://upload.wikimedia.org/wikipedia/en/thumb/6/6a/Mike_Wazowski.png/250px-Mike_Wazowski.png",   
    
    "Mark McGlinchey": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAw4NpdrcFFUcMPY7U6CQOynickrOo0wWJflxWCy68AP_b__nm03ZDEX2sIldG6lqueUJD&s",
    "Kev laaaa": "https://i.guim.co.uk/img/static/sys-images/Sport/Pix/pictures/2009/1/15/1232022588405/Kevin-Kilbane-001.jpg?width=465&dpr=1&s=none&crop=none",

    "Daniel Hirst": "https://ichef.bbci.co.uk/images/ic/1200x675/p07h17xl.jpg",

    "John Bridgeman": "https://i.ytimg.com/vi/Uj5iPDcRiUg/maxresdefault.jpg",
    "James King": "images/king.png",
    "Toby Munson": "https://static.wikia.nocookie.net/ttte/images/0/0c/MainTobyModel.png/revision/latest?cb=20250531164542",
    "Rory Scullin": "https://innerbody.imgix.net/Skull.png",
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
    ("Neil Roberton", "Jacob Stokes"),
("Neil Roberton", "James King"),
("Neil Roberton", "Rory Scullin"),
("Neil Roberton", "Toby Munson"),
("Neil Roberton", "Oliver Deverall"),
("Neil Roberton", "Mark McGlinchey"),
("Neil Roberton", "Steven Robinson"),
("John Bridgman", "Michael Dixon"),
("John Bridgman", "Daniel Hirst"),
("John Bridgman", "Jacob Stokes"),
("John Bridgman", "James King"),
("John Bridgman", "Toby Munson"),
("John Bridgman", "Oliver Deverall"),
("John Bridgman", "Mark McGlinchey"),
("John Bridgman", "Jamie Dobbs"),
("John Bridgman", "Steven Robinson"),
("John Bridgman", "Neil Roberton"),

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
    ("Oliver Deverall", "James King"),
    ("Steven Robinson", "Daniel Hirst"),
    ("Neil Roberton", "Jacob Stokes"),
    ("Neil Roberton", "James King"),
    ("Neil Roberton", "Rory Scullin"),
    ("Neil Roberton", "Toby Munson"),
    ("Neil Roberton", "Oliver Deverall"),
    ("Neil Roberton", "Steven Robinson"),
    ("Neil Roberton", "Mark McGlinchey"),

]

perfect_record_pairs = [
("Michael Dixon", "Jamie Dobbs"),
("Callum Goodyear", "Jacob Stokes"),
("Callum Goodyear", "James King"),
("Rory Scullin", "Daniel Hirst"),
("Rory Scullin", "Jacob Stokes"),
("Rory Scullin", "Jamie Dobbs"),
("Steven Robinson", "Jacob Stokes"),
("Neil Roberton", "Michael Dixon"),
("Neil Roberton", "Daniel Hirst"),
("Neil Roberton", "Callum Goodyear"),
("Neil Roberton", "Jamie Dobbs"),

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
    "A8": ["Callum Goodyear", "Rory Scullin", "Jacob Stokes", "Jamie Dobbs", "Steven Robinson"],
    "B8": ["Michael Dixon", "Daniel Hirst", "James King", "Mark McGlinchey", "Ringer"],
    "A9": ["Steven Robinson", "Jamie Dobbs", "Jacob Stokes", "Oliver Deverall", "Rory Scullin"],
    "B9": ["Callum Goodyear", "Daniel Hirst", "Michael Dixon", "Toby Munson", "Ringer"],

}
