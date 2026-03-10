import streamlit as st
import random
import time

# --- Page setup ---
st.set_page_config(page_title="Christmas Song Draw", layout="wide")
st.title("🎄 Christmas Party Song Draw 🎶")

# --- Participants and GIFs ---
participants = {
    "Gareth Evans": "https://i.makeagif.com/media/10-06-2014/flJZHM.gif",
    "Jacob Stokes": "https://i.pinimg.com/originals/20/a7/81/20a7813c6c5913b7112e992e0566c809.gif",
    "Mark Ross": "https://i.pinimg.com/originals/8c/4c/0d/8c4c0d2371f946da94fa24290ae99018.gif",
    "Neil Roberton": "https://img2.thejournal.ie/inline/2486714/original/?width=360&version=2486714",
    "Brett Cash": "https://media.tenor.com/6Hixx4SFAeQAAAAM/backing-you-get-yours.gif",
    "Daniel Hirst": "https://media.tenor.com/7z0XvJw2-bMAAAAM/kvara-khvicha.gif",
    "Mark McGlinchey": "https://media.tenor.com/8E-1U2A7xwQAAAAM/working-out-exercise.gif",
    "Callum Goodyear": "https://media.tenor.com/i4pEGvY7OqwAAAAM/goodyear-tires.gif",
    "Roxi Quinn": "https://media2.giphy.com/media/v1.Y2lkPTZjMDliOTUya2NxcWZnZ29kNXlqa2I4bnpyMmJlY2F0dGt2Y3RldjJhbGsyaGxqeiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zSUanrp1uZHfq/200.gif",
    "James Penney": "https://media2.giphy.com/media/v1.Y2lkPTZjMDliOTUyMzNveXVseGkzeGdzbXMwbGxlZ3drM2EyZnluMXBxcGI1azR4eDdvNSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xT9IgvEOwRzUcZDRiU/source.gif",
    "Charlotte McGregor": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGowM282eTByaTk4b3RsN3pka3JteTdld2lqYjVjdjhzeTlpaHZtMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26gJyIscAHtBNcc00/giphy.gif",
    "Luke Martin-Aspinall": "https://upload.wikimedia.org/wikipedia/en/3/3b/LMAManager2001coverart.jpg",
    "Toby Munson": "https://i.pinimg.com/originals/5a/c0/2e/5ac02ef52987875c8f1aba1bb2656e9e.gif",
    "Aradhana Mallick": "https://i.ebayimg.com/images/g/t4sAAOSwlJxn-tf2/s-l1200.jpg",
    "Amy Fouweather": "https://prettystyleofliving.wordpress.com/wp-content/uploads/2018/07/giphy-11.gif?w=620",
    "James King": "https://media.tenor.com/MpTy4knnxe8AAAAM/lebron-james-king-james.gif",
    "Jamie Dobbs": "https://media.tenor.com/oQ8VAfRNGqMAAAAM/fist-pump-jimmy-fallon.gif",
    "John Bridgman": "https://f4.bcbits.com/img/0002271315_36.jpg",
    "Michael Dixon": "https://pbs.twimg.com/profile_images/1213250965/M_Dixon_Come_Home_small.jpg",
    "Oliver Deverall": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkSFFiqlKtTMTO2JgVl11O4Ox7Q49kOnA-7w&s",
    "Rebecca Holmes": "https://media.tenor.com/67EGa-wMf5MAAAAM/sherlock-benedict-cumberbatch.gif",
    "Rory Scullin": "https://beehiiv-images-production.s3.amazonaws.com/uploads/asset/file/f0b318d4-b6c4-4e63-867f-6cf0f6906202/ScreenRecording_11-28-202417-44-29_1-ezgif.com-optimize.gif?t=1732886767",
    "Shiwoni Dona": "https://media.tenor.com/fvezf1pDkDoAAAAM/scared-pirate.gif",
    "Steven Robinson": "https://www.gif-vif.com/trending/i-think-you-should-leave-tim-robinson-steak-jodcntr6kou1bj0y.gif",
    "Hussain Jamali": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYJJluNOdiN2cWRQgCQjQI4ho15fQgj2OsnQ&s",
    "James Jose": "https://www.bluenote.com/wp-content/uploads/sites/956/2019/03/JoseJames_LeanOnMe_cover-500x500.jpg",

}

# --- Songs and GIFs ---
songs = {
    "All I Want For Christmas is You – Mariah Carey": "https://cdn.kqed.org/wp-content/uploads/sites/2/2023/12/Screen-Shot-2023-12-11-at-12.43.17-PM-2048x1340.png",
    "Merry Christmas Everybody – Slade": "https://m.media-amazon.com/images/I/61Q+XKwZv4L._UF894,1000_QL80_.jpg",
    "Merry Christmas Everyone – Shakin Stevens": "https://media0.giphy.com/media/v1.Y2lkPTZjMDliOTUyemt1cmx0Y3plNHdjYWNlMGRqMmFqdzRzam1vZDhldTFrb3J1cnpucSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/zgpxKtkVn3xZWRKBsv/giphy-downsized.gif",
    "Wonderful Christmas Time – Paul McCartney": "https://media1.giphy.com/media/3oz8xBz4crpQ5fNj5S/giphy.gif",
    "Happy Xmas (War is over) – John Lennon": "https://i.pinimg.com/originals/b8/91/a2/b891a2188702b6ed6afd99b51649bb43.gif",
    "Fairytale of New York – The Pogues ft Kirsty MacColl": "https://media.tenor.com/oQqd1_XeknEAAAAM/pogues-the-pogues.gif",
    "I Wish It Could Christmas Everyday! – Wizzard": "https://xmasyuleblog.wordpress.com/wp-content/uploads/2017/12/screen-shot-2017-12-14-at-19-51-45.png?w=451&h=310",
    "Last Christmas – Wham!": "https://64.media.tumblr.com/35e513970c25aad73ba631eeff9dd5dd/b6629316de02ca7d-c5/s540x810/70f3d78eb365b8c505156e27926c1a226b8f9e8c.gifv",
    "Thank God It’s Christmas – Queen": "https://i.makeagif.com/media/12-23-2020/dtmqim.gif",
    "It’s the Most Wonderful Time of the Year – Andy Williams": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8BbT9cOc1UaiL0Vry4HBbygsvkWxonhfQRQ&s",
    "Santa Tell Me - Ariana Grande": "https://i.pinimg.com/originals/7a/e1/9b/7ae19ba42af4d954f64ec98b4123bd77.gif",
    "Baby It’s Cold Outside – Tom Jones & Cerys Matthews": "https://i.pinimg.com/originals/23/5a/7e/235a7e4699428a3df5607eae0b788b6f.gif",
    "Let It Snow! – Dean Martin": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRliog6JFhMLsT2sMfV2mTI72fwSY6M19O1sQ&s",
    "Christmas Time (Don’t Let The Bells End) – The Darkness": "https://i.makeagif.com/media/4-07-2017/PVRKuq.gif",
    "Feliz Navidad - Jose Feliciano": "https://media2.giphy.com/media/v1.Y2lkPTZjMDliOTUyZzNoMXZnb3d1NXU3aWExajZlZXIzcjB0b3h4Z2cyNTluZmdjNXllMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/y1nqPmQ94ymcZkLeGP/giphy.gif",
    "Snowman - Sia": "https://i.makeagif.com/media/12-22-2023/KpVVFw.gif",
    "Merry Christmas - Elton John & Ed Sheeran": "https://hollywoodlife.com/wp-content/uploads/2021/12/Elton-John-EdSheeran.gif",
    "Stop The Cavalry - Jona Lewie": "https://www.tv80s.com/wp-content/uploads/2015/04/jona-lewie-stop-the-cavalry.jpg",
    "Stay Another Day - East 17": "https://i.pinimg.com/originals/79/df/c8/79dfc8a13dd4dac0dc05a79dc5ba95e8.gif",
    "Lonely This Christmas - Mud": "https://i.makeagif.com/media/11-16-2017/XuDjzC.gif",
    "Driving Home for Christmas - Chris Rea": "https://i.makeagif.com/media/12-19-2023/lB88bi.gif",
    "It's Beginning to Look a Lot Like Christmas - Michael Buble": "https://media0.giphy.com/media/v1.Y2lkPTZjMDliOTUyN2xobGJkNDQyazcxdzVidDdzdHdwbTA4bjdianJpMnJodjE1NTdhMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/cnhih1AM9M7z9oEQva/giphy.gif",
    "Jingle Bell Rock - Bobby Helms": "https://media1.giphy.com/media/H3YUiJcXWBQra8CvR3/giphy.gif",
    "Mistletoe - Justin Bieber": "https://i0.wp.com/media1.giphy.com/media/CwAnLuSBarO6s/giphy.gif",
    "Santa Baby - Kylie Minogue": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRtjgWZQ_XrfZ-zurO0Oe1GGvFBPJQ_BnJrA&s",
    "Deck the halls - Nat King Cole": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWI_-bbaREF5W0l6jog7lQKmAMEoqg15VjcA&s"
}

# --- Layout ---
col1, col2 = st.columns([3, 1])
main_box = col1.empty()
gif_box = col1.empty()
caption_box = col1.empty()
log_box = col2.empty()
draw_log = []


# --- Helper functions ---
def show_text(text, delay=3):
    existing = st.session_state.get('text_log', [])
    existing.append(text)
    st.session_state['text_log'] = existing
    main_box.markdown('<br>'.join(existing), unsafe_allow_html=True)
    time.sleep(delay)


def clear_text():
    st.session_state['text_log'] = []
    main_box.empty()


# Initialize text log
if 'text_log' not in st.session_state:
    st.session_state['text_log'] = []


def show_gif(gif_url, delay=4):
    gif_box.image(gif_url, width=400)
    time.sleep(delay)
    gif_box.empty()


def log_draw(person, song):
    draw_log.append(f"**{person}** → {song}")
    log_box.markdown('<br>'.join(draw_log), unsafe_allow_html=True)


# --- Start Draw ---
if st.button("🎬 Begin the Song Draw!"):
    show_text("Welcome to the Christmas Song Draw! 🎄")

    show_text("Here to present the draw is ....")
    show_text("She moved to Paris at the age of 24 after leaving Warsaw's Flying University")
    show_gif(
        "https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcTk5nISCfvw5x2gI2ZNtYKcsqreYbuVnCNDmO06ygQ6YVG7HFxp_xpFwPpUbqbEfDKd")
    show_text("It is Marie Curie")
    show_text("Alongside her usual Parisian partner, they are like Ant and Dec these two")
    show_gif("https://ichef.bbci.co.uk/ace/standard/624/cpsprodpb/62B6/production/_89407252_gettyimages-502062386.jpg")
    show_text("Yes, Mamadou, hello how are you")
    show_text("Cheers Marie, I'd just like to be the first to congratulate you on your 2nd Nobel Prize")
    show_text("I appreciate that Mamadou. How is life in Georgia with Torpedo Kutasi?")
    show_text("It is great. Enough small talk. Let's discuss how this is going to work")
    show_text("---------------------------------------------------", 1)

    show_text("There are 24 players, and 24 songs. Each will be randomly paired up so each player gets a song")
    show_text("The FIRST person to notify Mark/other players that they have heard their song will win")
    show_text("Great, as easy as that. Are there any time stipulations Mamadou?")
    show_text("Brilliant question Marie, yes, the 'game' starts after 9pm.")
    clear_text()

    show_text("Let us take a sneak peak into what we are to expect this evening")

    show_gif("https://www.spice-escapes.co.uk/wp-content/uploads/2025/09/pexels-pixabay-532826-scaled.jpg")
    show_gif("https://hartley-botanic.co.uk/wp-content/uploads/2019/07/Image-2-July-2019-1.jpg")
    show_gif("https://cdn.assets.prezly.com/666f01bd-22b5-4f6e-9e34-2ac7fb6f458e/Belgaimage-137271077.jpg")
    clear_text()

    show_text("Lets have an introduction to some of the songs on show today")
    show_text("We're talking your Slades of the world, Stevens certainly Shakin', and dont forget about Mariah")
    show_text("Some newer songs make the cut, Ariana Grade, Ed Sheeran and Sia will be making appearances")

    show_text("Right, here we go, onto the main event")

    clear_text()

    # --- Shuffle participants and songs ---
    participant_list = list(participants.keys())
    song_list = list(songs.keys())
    random.shuffle(participant_list)
    random.shuffle(song_list)

    # --- Assign songs ---
    for person, song in zip(participant_list, song_list):
        show_text(f"Next up......", 2)
        show_gif(participants[person])
        show_text(f"You guessed it, it's...**{person}**", 2)

        show_text(f"And the song assigned is......", 2)
        show_gif(songs[song])
        show_text(f"That's right, it's...**{song}**")

        log_draw(person, song)
        clear_text()

    show_text("Woaahhhh what is that!!")
    show_gif("https://media.harrypotterfanzone.com/golden-snitch-gif.gif")
    show_text("Whoever catches it gets to trade songs to any they wish")
    show_text("Oh wow that's amazing, lets watch the drama unfold")
    show_gif("https://pa1.aminoapps.com/5867/e186c3d8054cec3f6aa44a5f1679185e51fce90e_hq.gif")
    show_text("I can't wait to see who catches it")
    show_text("This live draw has been the highlight of my day")
    show_text("And this is the cherry on top")

    for i in range(2):
        picker = random.choice(participant_list)
        show_gif(participants[picker])
        show_text(f"{picker} tries to catch the snitch...")
        if i == 1:
            show_gif(
                "https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUybzl5ZDUzYWd0bmltMDlqdG1wZnlybXUwbWxob2M0d2tyMHZ4aWc4bCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/13ywPzPJdfhmBG/200w.gif")
        else:
            show_gif(
                "https://metro.co.uk/wp-content/uploads/2019/12/Catch-1392.gif?w=440&h=248&crop=1&quality=90&strip=all&zoom=1")
        show_text("Oh no, they have dropped it!")

        participant_list.remove(picker)

    # Third player catches it
    winner = random.choice(participant_list)
    show_gif(participants[winner])
    show_text(f"{winner} goes for it...")

    show_text(f"🎉 {winner} catches the snitch! They can trade songs as they wish! 🎉")

    show_text("🎉 All songs have been assigned! 🎉")
    st.balloons()
