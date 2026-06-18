import pandas as pd
import streamlit as st

from data_paths import AVAILABILITY_FILE, csv_repo_path
from github_csv import load_csv, save_csv
from roster import normalize_player_name

AVAILABLE_DATES = [
    "July Wednesday 1st (ENG group winners R32 5PM)",
    "July Thursday 2nd",
    
    "July Tuesday 7th (ENG group 3RD R32 9PM)",
    "July Wednesday 8th",
    "July Thursday 9th",
    
    "July Tuesday 14th (ENG group RU SF 8PM)",
    "July Wednesday 15th (ENG group winners/3RD SF 8PM)",
    "July Thursday 16th",
    
    "July Tuesday 21st",
    "July Wednesday 22nd",
    "July Thursday 23rd",

    "July Tuesday 28th",
    "July Wednesday 29th",
    "July Thursday 30th",
    
    "I am unable to play"
]


def render_availability_tab():
    st.info("Enter a player name, tick the dates they can play, and submit.")

    available_dates = AVAILABLE_DATES
    existing_df = _load_availability()

    with st.form("availability_form", clear_on_submit=False):
        player_name = st.text_input("Player name").strip()

        st.markdown("### Available dates")
        selected_dates = []
        columns = st.columns(2)
        for index, available_date in enumerate(available_dates):
            with columns[index % 2]:
                if st.checkbox(available_date, key=f"availability_{available_date}"):
                    selected_dates.append(available_date)

        submitted = st.form_submit_button("Submit")

    if submitted:
        if not player_name:
            st.error("Please enter a player name.")
        else:
            updated_df = _upsert_availability(existing_df, player_name, selected_dates)
            save_csv(csv_repo_path(AVAILABILITY_FILE), updated_df, f"Update availability for {player_name}")
            existing_df = updated_df
            st.success(f"Saved availability for {player_name}.")

    st.divider()
    _render_completion_lists(existing_df)
    st.divider()
    st.markdown("### Submitted availability")
    if existing_df.empty:
        st.caption("No availability submitted yet.")
    else:
        st.dataframe(existing_df.sort_values("Player").reset_index(drop=True), hide_index=True, width="stretch")
        st.divider()
        st.markdown("### Availability by date")
        st.bar_chart(_build_availability_chart(existing_df, available_dates), x="Date", y="Count", width="stretch")


def _load_availability():
    df = load_csv(csv_repo_path(AVAILABILITY_FILE), ["Player", "Available Dates"])
    if df.empty:
        return df

    df = df.copy()
    df["Player"] = df["Player"].map(normalize_player_name)
    df = df.drop_duplicates(subset=["Player"], keep="last")
    return df


def _upsert_availability(existing_df, player_name, selected_dates):
    player_name = normalize_player_name(player_name)
    available_dates_value = ", ".join(selected_dates) if selected_dates else "No dates selected"
    new_row = pd.DataFrame(
        [{"Player": player_name, "Available Dates": available_dates_value}]
    )

    if existing_df.empty:
        return new_row

    filtered_df = existing_df[existing_df["Player"].str.casefold() != player_name.casefold()].copy()
    return pd.concat([filtered_df, new_row], ignore_index=True)


def _build_availability_chart(existing_df, available_dates):
    counts = {available_date: 0 for available_date in available_dates}

    for dates_value in existing_df["Available Dates"].fillna(""):
        submitted_dates = [item.strip() for item in str(dates_value).split(",") if item.strip()]
        for submitted_date in submitted_dates:
            if submitted_date in counts:
                counts[submitted_date] += 1

    return pd.DataFrame(
        [{"Date": available_date, "Count": counts[available_date]} for available_date in available_dates]
    )


def _render_completion_lists(existing_df):
    submitted_players = sorted(
        existing_df.get("Player", pd.Series(dtype=str)).dropna().tolist()
    )

    st.markdown("### Submitted players")
    if submitted_players:
        st.write(submitted_players)
    else:
        st.caption("No availability submissions yet.")
