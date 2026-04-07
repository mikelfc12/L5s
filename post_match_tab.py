import pandas as pd
import streamlit as st

from github_csv import load_csv, save_csv

GAMEWEEK = "GW9"
POST_MATCH_FILE = "post_match.csv"
POST_MATCH_PLAYERS = [
    "Rory Scullin",
    "Steven Robinson",
    "Callum Goodyear",
    "Toby Munson",
    "Michael Dixon",
    "Oliver Deverall",
    "Daniel Hirst",
    "Jacob Stokes",
    "Jamie Dobbs",
    "Josh",
]
RATING_OPTIONS = [1, 2, 3, 4, 5, 6, 7]


def render_post_match_tab():
    st.info("Complete every question before submitting the post-match form.")
    existing_df = _load_post_match_submissions()

    with st.form("post_match_form", clear_on_submit=False):
        player_name = st.text_input("Player name").strip()
        goals_scored = st.number_input("1. How many goals did you score?", min_value=0, step=1)

        motm = st.selectbox(
            "2. Who was your MOTM?",
            options=["Select a player"] + POST_MATCH_PLAYERS,
            index=0,
        )
        gotg = st.selectbox(
            "3. Who scored the GOTG?",
            options=["Select a player"] + POST_MATCH_PLAYERS,
            index=0,
        )

        st.markdown("### 4. Player Ratings")
        ratings = {}
        for player in POST_MATCH_PLAYERS:
            ratings[player] = st.radio(
                player,
                options=RATING_OPTIONS,
                index=None,
                horizontal=True,
                key=f"post_match_rating_{player}",
            )

        submitted = st.form_submit_button("Submit")

    if submitted:
        validation_error = _validate_submission(player_name, motm, gotg, ratings)
        if validation_error:
            st.error(validation_error)
        else:
            updated_df = _append_post_match_submission(
                existing_df,
                player_name,
                int(goals_scored),
                motm,
                gotg,
                ratings,
            )
            save_csv(POST_MATCH_FILE, updated_df, f"Add post-match submission for {player_name}")
            st.success(f"Saved post-match answers for {player_name}.")


def _validate_submission(player_name, motm, gotg, ratings):
    if not player_name:
        return "Please enter a player name."
    if motm == "Select a player":
        return "Please choose a MOTM."
    if gotg == "Select a player":
        return "Please choose who scored the GOTG."
    if any(rating is None for rating in ratings.values()):
        return "Please provide a rating for every player."
    return None


def _load_post_match_submissions():
    return load_csv(POST_MATCH_FILE, _submission_columns())


def _append_post_match_submission(existing_df, player_name, goals_scored, motm, gotg, ratings):
    submission_row = {
        "Gameweek": GAMEWEEK,
        "Player Name": player_name,
        "Goals Scored": goals_scored,
        "MOTM": motm,
        "GOTG": gotg,
    }
    submission_row.update({f"Rating - {player}": rating for player, rating in ratings.items()})

    new_row_df = pd.DataFrame([submission_row])
    if existing_df.empty:
        return new_row_df
    return pd.concat([existing_df, new_row_df], ignore_index=True)


def _submission_columns():
    return [
        "Gameweek",
        "Player Name",
        "Goals Scored",
        "MOTM",
        "GOTG",
        *[f"Rating - {player}" for player in POST_MATCH_PLAYERS],
    ]
