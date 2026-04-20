import streamlit as st

import display_functions as disp_f
import functions as func
import variables as v

TEAM_A_STARTER = ["Rory Scullin", "Steven Robinson"]
TEAM_B_STARTER = ["Callum Goodyear", "Toby Munson"]
POT_1 = ["Michael Dixon", "Josh"]
POT_2 = ["Jamie Dobbs", "Oliver Deverall"]
POT_3 = ["Daniel Hirst", "Jacob Stokes"]


def render_draw_tab():
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
            ("keep", POT_1),
            ("keep", POT_2),
            ("split", POT_3),
        )
        print("A:", team_a)
        print("B:", team_b)

        disp_f.say("Welcome to the **4MOST 5-a-Side Draw**", text_box)

        # Introduce hosts
        disp_f.say("Introducing our first host", text_box)
        disp_f.say("All the way from Chester and Ellesmere Port", text_box)
        disp_f.say("He's made time for us on this Tuesday day before Wednesday", text_box)
        gif_box.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCtWodEx7DX9LCkK8-NrgfMDsLcx7PFcmViQ&s")

        disp_f.say("Famous for his luxurious desserts", text_box)
        disp_f.say("Hi guys, just back from Benidorm, lovely bit of tan from the sun one before the moon", text_box)
        gif_box.empty()
        disp_f.clear_text_box(text_box)



        
        disp_f.say("And alongside him, ", text_box)
        gif_box.image("images/host.png")
        disp_f.pause(10)
        disp_f.say("You guessed it, it's Aaron Lennon", text_box)
        gif_box.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRDjKNvTVpN-c0scImvgHEdjJh5rTP_ssAW3stGlCj5TVNZVrConHhKke2-ap5cONLsgfme10_AFBenRybBoc-3PO_XMj_FSt4g6izRcg&s=10")
        gif_box.empty()

        disp_f.say("How we doing Leeeeedsssssss", text_box)
        

        disp_f.say("We have some huge news to be shared", text_box)
        disp_f.say("We're going global...", text_box)
        disp_f.say("Later today, a link to this hot off the press website will drop", text_box)
        disp_f.say("Full of all the stats you desire, forms and more in the pipeline", text_box)
        disp_f.say("Comments, improvements and any bugs you spot, please shout", text_box)
        disp_f.say("Huge", text_box)
        disp_f.say("Lovely day for it", text_box)

        disp_f.clear_text_box(text_box)

        disp_f.say("Speaking of which, lets have a weather report", text_box)
        gif_box.image("images/weather.png")
        disp_f.pause(5)
        gif_box.empty()

        disp_f.say("16 degrees lets gooooo", text_box)
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
