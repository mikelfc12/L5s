import streamlit as st

import display_functions as disp_f
import functions as func
import variables as v


TEAM_A_STARTER = []
TEAM_B_STARTER = []
POT_1 = ["Daniel Hirst", "Jacob Stokes"]
POT_2 = ["Callum Goodyear", "Toby Munson", "Oliver Deverall", "Steven Robinson"]
POT_3 = ["Michael Dixon", "James King","Jamie Dobbs", "Rory Scullin"]


def render_draw_tab():
    print(30*"-")
    col1, col2, col3 = st.columns([3, 2, 3])
    with col1:
        st.markdown("### 🟥 Team A")
        team_a_box = st.empty()
    with col2:
        text_box = st.empty()
        gif_box = st.empty()
        caption_box = st.empty()
        center_box = st.empty()
    with col3:
        st.markdown("### 🟦 Team B")
        team_b_box = st.empty()

    team_a_drawn, team_b_drawn = [], []

    if st.button("🎬 Begin the Show!"):
        st.session_state["log"] = []

        team_a, team_b = func.generate_teams(
            TEAM_A_STARTER,
            TEAM_B_STARTER,
            v.previous_teams,
            ("split", POT_1),
            ("split", POT_2),
            ("split", POT_3),
        )
        print("A:", team_a)
        print("B:", team_b)

        disp_f.say("Welcome to the **4MOST 5-a-Side Draw**", text_box)

        # Introduce hosts
        disp_f.say("Introducing our first host", text_box)
        disp_f.say("All the way from Canada", text_box)
        disp_f.say("You might be seeing more of them in Portugal", text_box)
        gif_box.image("https://winningmoves.co.uk/cdn/shop/files/5675b772-0247-4697-8696-e308afb2a6cf.jpg?v=1713174916")
        gif_box.empty()
        disp_f.say("11 stage presence, lets see how you can perform on the biggest stage of all", text_box)
        disp_f.say("The 4most 5 a side LIVE draw", text_box)
        disp_f.say("Hey guyyssssss", text_box)
        gif_box.empty()
        disp_f.clear_text_box(text_box)
        disp_f.say("Cheers Carly", text_box)

        disp_f.say("And alongside her, ", text_box)
        disp_f.say("One of the worlds worst guys", text_box)
        disp_f.say("Actually hate this guy", text_box)
        gif_box.image("https://i.redd.it/kmb1j74ojhcb1.jpg")

        disp_f.say("Do you have any quiz questions for us lads?", text_box)
        disp_f.say("Rory and who other have the best 2 player combination with 4 wins from 4 and a GD of 14??", text_box)
        disp_f.pause(10)
        disp_f.say("Yep you guessed it, it's last weeks MOTM, ya boy Stokes", text_box)
        gif_box.empty()

        disp_f.say("More stats like this corker on the site", text_box)


        disp_f.say("Lovely day for it", text_box)
        disp_f.clear_text_box(text_box)

        disp_f.say("Speaking of which, lets have a weather report", text_box)
        gif_box.image("images/weather.png")
        disp_f.pause(5)
        gif_box.empty()

        disp_f.say("Sunny init neymar", text_box)
        disp_f.clear_text_box(text_box)

        disp_f.say("Right, lets get into the draw...", text_box)
        disp_f.clear_text_box(text_box)

        remaining_players = team_a + team_b
        disp_f.show_center(remaining_players, center_box)

        for a_player, b_player in zip(team_a, team_b):
            disp_f.pick_work(
                "A",
                a_player,
                gif_box,
                remaining_players,
                team_a_drawn,
                team_b_drawn,
                team_a_box,
                team_b_box,
                caption_box,
                center_box,
            )
            disp_f.pause(5)

            disp_f.pick_work(
                "B",
                b_player,
                gif_box,
                remaining_players,
                team_a_drawn,
                team_b_drawn,
                team_a_box,
                team_b_box,
                caption_box,
                center_box,
            )
            disp_f.pause(5)

        disp_f.say("Some stats on these teams please, if any", text_box)

        _render_team_alerts("Team A", team_a)
        _render_team_alerts("Team B", team_b)

        st.success("🏁 The draw is complete!")
        st.balloons()


def _render_team_alerts(team_label, team):
    never_won = func.check_pairs(team, v.never_won_pairs)
    perfect_record = func.check_pairs(team, v.perfect_record_pairs)
    never_played = func.check_pairs(team, v.never_played_pairs)

    st.markdown(f"### {team_label} Alerts")

    if never_played:
        for p1, p2 in never_played:
            st.warning(f"{p1} & {p2} have never played together")

    if never_won:
        for p1, p2 in never_won:
            st.error(f"{p1} & {p2} have NEVER won together")

    if perfect_record:
        for p1, p2 in perfect_record:
            st.success(f"{p1} & {p2} have a 100% record together")

    if not never_won and not perfect_record and not never_played:
        st.info(f"No special pair alerts for {team_label}")
