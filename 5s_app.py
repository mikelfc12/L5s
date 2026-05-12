import pandas as pd
import streamlit as st

from availability_tab import render_availability_tab
from data_paths import RAW_DATA_FILE
from draw_tab import render_draw_tab
from post_match_tab import render_post_match_tab
from stats_tab import render_stats_tab

raw_data_df = pd.read_csv(RAW_DATA_FILE)


def initialise_session_state():
    if "rpt" not in st.session_state:
        st.session_state.rpt = False
    if "unbeaten_combinations" not in st.session_state:
        st.session_state.unbeaten_combinations = False
    st.session_state["raw_data_df"] = raw_data_df


def render_app_styles():
    st.markdown(
        """
        <style>
        @keyframes drift-left {
          from {transform: translateX(0); opacity: 1;}
          to {transform: translateX(-400px); opacity: 0;}
        }
        @keyframes drift-right {
          from {transform: translateX(0); opacity: 1;}
          to {transform: translateX(400px); opacity: 0;}
        }
        .player {
          font-size: 1.3rem;
          margin: 0.4rem;
          transition: all 1s ease-in-out;
        }
        .left { color: red; animation: drift-left 2s forwards; }
        .right { color: blue; animation: drift-right 2s forwards; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="5-a-Side Draw", layout="wide")
    st.title("⚽ The Official 4MOST 5-a-Side Draw ⚽")

    initialise_session_state()
    render_app_styles()

    draw_tab, stats_tab, availability_tab, post_match_tab = st.tabs(
        ["Draw", "Statistics", "Availability", "Post Match"]
    )

    with draw_tab:
        render_draw_tab()

    with stats_tab:
        render_stats_tab(raw_data_df)

    with availability_tab:
        render_availability_tab()

    with post_match_tab:
        render_post_match_tab()


if __name__ == "__main__":
    main()
