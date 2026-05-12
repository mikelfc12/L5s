import pandas as pd
import streamlit as st

from data_paths import POST_MATCH_FILE, csv_repo_path
from github_csv import load_csv, save_csv
from roster import CANONICAL_PLAYERS, normalize_player_name

GAMEWEEK = "GW10"
POST_MATCH_PLAYERS = CANONICAL_PLAYERS
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

        gotg_desc = st.text_input("Describe the goal")

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
        validation_error = _validate_submission(player_name, motm, gotg, gotg_desc, ratings)
        if validation_error:
            st.error(validation_error)
        else:
            updated_df = _append_post_match_submission(
                existing_df,
                player_name,
                int(goals_scored),
                motm,
                gotg,
                gotg_desc,
                ratings,
            )
            save_csv(csv_repo_path(POST_MATCH_FILE), updated_df, f"Add post-match submission for {player_name}")
            st.success(f"Saved post-match answers for {player_name}.")
            existing_df = updated_df

    st.divider()
    _render_completion_lists(existing_df)


def _validate_submission(player_name, motm, gotg, gotg_desc, ratings):
    if not player_name:
        return "Please enter a player name."
    if normalize_player_name(player_name) not in CANONICAL_PLAYERS:
        return "Please enter a recognised player name."
    if motm == "Select a player":
        return "Please choose a MOTM."
    if gotg == "Select a player":
        return "Please choose who scored the GOTG."
    if not gotg_desc.strip():
        return "Please describe the goal of the game."
    if any(rating is None for rating in ratings.values()):
        return "Please provide a rating for every player."
    return None


def _load_post_match_submissions():
    df = load_csv(csv_repo_path(POST_MATCH_FILE), _submission_columns())
    if df.empty:
        return df

    df = df.copy()
    df["Player Name"] = df["Player Name"].map(normalize_player_name)
    df = df.drop_duplicates(subset=["Gameweek", "Player Name"], keep="last")
    return df


def _append_post_match_submission(existing_df, player_name, goals_scored, motm, gotg, gotg_desc, ratings):
    player_name = normalize_player_name(player_name)
    submission_row = {
        "Gameweek": GAMEWEEK,
        "Player Name": player_name,
        "Goals Scored": goals_scored,
        "MOTM": motm,
        "GOTG": gotg,
        "GOTG Description": gotg_desc.strip(),
    }
    submission_row.update({f"Rating - {player}": rating for player, rating in ratings.items()})

    new_row_df = pd.DataFrame([submission_row])
    if existing_df.empty:
        return new_row_df
    filtered_df = existing_df[
        ~(
            (existing_df["Gameweek"] == GAMEWEEK)
            & (existing_df["Player Name"].str.casefold() == player_name.casefold())
        )
    ].copy()
    return pd.concat([filtered_df, new_row_df], ignore_index=True)


def _submission_columns():
    return [
        "Gameweek",
        "Player Name",
        "Goals Scored",
        "MOTM",
        "GOTG",
        "GOTG Description",
        *[f"Rating - {player}" for player in POST_MATCH_PLAYERS],
    ]


def _render_completion_lists(existing_df):
    current_week_df = existing_df[existing_df["Gameweek"] == GAMEWEEK].copy()
    submitted_players = sorted(
        player for player in current_week_df.get("Player Name", pd.Series(dtype=str)).dropna().tolist()
        if player in CANONICAL_PLAYERS
    )

    st.markdown(f"### Submitted for {GAMEWEEK}")
    if submitted_players:
        st.write(submitted_players)
    else:
        st.caption("No post-match submissions yet.")
