import streamlit as st

import display_functions as disp_f
import functions as func
import statistics as s
import variables as v


TEAM_A_STARTER = []
TEAM_B_STARTER = []
POT_1 = ["Daniel Hirst", "Josh Ringer"]
POT_2 = ["Callum Goodyear", "Oliver Deverall"]
POT_3 = ["Michael Dixon", "Jamie Dobbs"]
POT_4 = ["Mark McGlinchey", "Kev laaaa"]
POT_5 = ["Jacob Stokes", "Steven Robinson"]

FIRST_HOST_IMAGE = "images/host1.jpg"
SECOND_HOST_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSynfA12iDA9sBWfhdOKiE3XTyVCOL9kfW9jwWXub5fvAqcwZ0YZl0MG2kfObdHmb1glLrYLIGYAibuE32UUhroR1HMdwM8fdfmbShZXg&s=10"


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
            ("split", POT_4),
            ("split", POT_5)
        )

        print("A:", team_a)
        print("B:", team_b)

        disp_f.say("Welcome to the **4MOST 5-a-Side Draw**", text_box)

        disp_f.say("A quick caveat, I wrote this on Monday so if something goes wrong (shrug emoji)", text_box)
        disp_f.say("The urls for some of the images driving me insane so it is what it issss", text_box)

        # Introduce hosts
        disp_f.say("Introducing our first host", text_box)
        disp_f.say("We saw a lot of her last week", text_box)
        gif_box.image(FIRST_HOST_IMAGE)
        disp_f.pause(5)
        gif_box.empty()
        disp_f.say("It's Dusty Springfield", text_box)
        disp_f.clear_text_box(text_box)

        disp_f.say("And alongside her, ", text_box)
        disp_f.say("One of the worst groups going", text_box)
        disp_f.say("How did I finish below these gimps in music league what the hell", text_box)
        gif_box.image(SECOND_HOST_IMAGE)
        disp_f.clear_text_box(text_box)
        disp_f.say("It's Las Ketchup", text_box)
        disp_f.say("the fuck", text_box)
        disp_f.say("I know right", text_box)
        gif_box.empty()
        disp_f.clear_text_box(text_box)

        disp_f.say("Lovely day for it", text_box)
        disp_f.clear_text_box(text_box)

        disp_f.say("Speaking of which, lets have a weather report", text_box)
        gif_box.image("images/weather.png")
        disp_f.pause(5)
        gif_box.empty()

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

        pair_records = s.generate_pair_records(st.session_state["raw_data_df"])
        _render_team_alerts("Team A", team_a, pair_records)
        _render_team_alerts("Team B", team_b, pair_records)

        st.success("🏁 The draw is complete!")
        st.balloons()


def _render_team_alerts(team_label, team, pair_records):
    never_won = func.check_pairs(team, pair_records["never_won"])
    perfect_record = func.check_pairs(team, pair_records["perfect_record"])
    never_played = func.check_pairs(team, pair_records["never_played"])

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
