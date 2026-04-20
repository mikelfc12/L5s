
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from graphing_funcs import _render_comp_chart
import pandas as pd

def create_graph_title(players):
    if len(players) == 1:
        return f"Stats for {players[0]}"
    title = "Comparison of "
    penultimate_player = players[-2]
    last_player = players[-1]
    for player in players:
        if player == last_player:
            title += f"{player}"
        elif player == penultimate_player:
            title += f"{player} and "
        else:
            title += f"{player}, "
    return title

          

def _grab_chart(df, players, type_of_graph):
    #players = ["Daniel Hirst", "Jacob Stokes"]
    if type_of_graph == "Radar":
        recoloured_plot = _render_comp_chart(df, players, 'rank')
    else:
        recoloured_plot = _render_comp_chart(df, players, 'rank', False)

    recoloured_plot.update_layout(
        {'legend_font_size':20,
         'font_size':18,
        },
        #plot_bgcolor = 'rgba(0,0,0,0)',
        #paper_bgcolor = 'rgba(0,0,0,0)',
        title = create_graph_title(players)
    )

    st.plotly_chart(
        figure_or_data = recoloured_plot,
        height = 900, 
        #width = 1800,
        theme = None,
        on_select = "ignore",
    )


def _render_player_comparisons(df: pd.DataFrame):
    st.title("Player Comparison Tool")
    list_of_players = df["Name"].unique()
    chosen_players = list_of_players[[0, 10]]
    graph_type = "Radar"
    # with st.sidebar: interesting but not right for this
    formcol, graphcol = st.columns([0.2,0.8])
    with formcol:
        with st.form("my form"):
            st.form_submit_button('Update Comparison')
            graph_type = st.radio("Plot type:", ["Radar","Bar"])
            chosen_players = st.multiselect(
                "Select players to compare:",
                list_of_players,
                key = "chosen_players",
            )
    with graphcol:
        if chosen_players:
                _grab_chart(df, chosen_players, graph_type)
        else:
            st.text("NO PLAYERS SELECTED")
