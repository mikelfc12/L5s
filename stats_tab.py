import io
import time
import urllib.request
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import Circle
from player_comp_tab import _render_player_comparisons # Think we should store the _render funcs in their own files

import display_functions as disp_f
import statistics as s

BALL_URL = (
    "https://assets.streamlinehq.com/image/private/w_512,h_512,ar_1/"
    "f_auto/v1/icons/7/soccer-ball-gapr651upnuseroqnw7ppl.png/"
    "soccer-ball-gsnnt0o2y4wtvehff0ckg.png?_a=DATAiZAAZAA0"
)


def render_stats_tab(raw_data_df):
    st.info("Stats")
    league_table, latest_match, player_combinations, charts_over_time, formation, player_comp_tab, raw_data_tab = st.tabs(
        ["League Table", "Last match", "Player Combinations", "Charts over time", "Formations", "Player Comparisons","View Raw Data"]
    )

    with league_table:
        _render_league_table(raw_data_df)

    with latest_match:
        _render_latest_match(raw_data_df)

    with player_combinations:
        _render_player_combinations(raw_data_df)

    with charts_over_time:
        _render_charts_over_time(raw_data_df)

    with formation:
        _render_formation(raw_data_df)

    with player_comp_tab:
        _render_player_comparisons(raw_data_df)

    with raw_data_tab:
        st.dataframe(raw_data_df, hide_index=True)


def _render_league_table(raw_data_df):
    player_table = s.convert_to_player_table(raw_data_df)
    format_dict = {
        **{col: "{:.2f}" for col in ["Avg_Rating", "GPG", "Ave TGF", "Ave TGA", "Ave TGD", "Ave MOTM", "Ave GOTG"]},
        **{col: "{:.1%}" for col in ["Win %", "% of team goals", "% of total goals"]},
    }

    st.toggle("Remove part timers", key="rpt")
    table = player_table.copy()

    if st.session_state.rpt:
        player_table_3plus = table[(table["Played"] >= 3) & (table["Name"] != "Ringer")].copy()
        player_table_under3 = table[(table["Played"] < 3) | (table["Name"] == "Ringer")].copy()

        player_table_3plus["Position"] = range(1, len(player_table_3plus) + 1)
        player_table_under3["Position"] = range(1, len(player_table_under3) + 1)

        st.dataframe(_style_player_table(player_table_3plus, format_dict), hide_index=True)
        st.divider()
        st.dataframe(_style_player_table(player_table_under3, format_dict), hide_index=True)
        return

    all_players = table.copy()
    all_players["Position"] = range(1, len(all_players) + 1)
    st.dataframe(_style_player_table(all_players, format_dict), hide_index=True)


def _style_player_table(table, format_dict):
    return (
        table.style.format(format_dict)
        .set_properties(
            subset=["Played", "Wins", "Draws", "Losses", "Points", "Win %"],
            **{"background-color": "#f8d7da"},
        )
        .set_properties(
            subset=["Goals", "GPG", "% of team goals", "% of total goals"],
            **{"background-color": "#7bf542"},
        )
        .set_properties(
            subset=["Team_GF", "Team_GA", "Team_GD", "Ave TGF", "Ave TGA", "Ave TGD"],
            **{"background-color": "#f5cb42"},
        )
        .set_properties(
            subset=["MOTM", "Ave MOTM", "GOTG", "Ave GOTG"],
            **{"background-color": "#f0faa2"},
        )
        .map(disp_f.colour_negative_red)
    )


def _render_latest_match(raw_data_df):
    col1, col2 = st.columns([1, 1])
    with col1:
        last_match_stats = s.last_game_stats(raw_data_df)
        styled = last_match_stats.style.format(
            {"Rating": "{:.2f}", "MOTM": "{:.0f}", "GOTG": "{:.0f}"}
        ).apply(disp_f.highlight_team_a, axis=1)
        st.dataframe(styled, hide_index=True)

    with col2:
        st.markdown("### Information about any key ratings")
        buffer_average = st.radio("Select % within for average", [1, 2.5, 5, 7.5, 10], horizontal=True)

        aggregated_df = raw_data_df.groupby("Name").agg(
            Max_R=("Rating", "max"),
            Min_R=("Rating", "min"),
            Mean_R=("Rating", "mean"),
        ).reset_index()
        summary_df = aggregated_df.merge(last_match_stats, on="Name", how="left")

        for _, row in summary_df.iterrows():
            latest = row["Rating"]
            if latest != latest:
                continue

            gap = buffer_average / 100
            within_pct = abs(latest - row["Mean_R"]) <= gap * row["Mean_R"]

            if latest == row["Max_R"]:
                st.success(f"ℹ️ {row['Name']} recorded their highest rating ({latest:.2f}).")
            elif latest == row["Min_R"]:
                st.error(f"ℹ️ {row['Name']} recorded their lowest rating ({latest:.2f}).")
            elif within_pct:
                st.warning(
                    f"ℹ️ {row['Name']}'s latest rating ({latest:.2f}) is within {gap * 100}% of "
                    f"their average ({row['Mean_R']:.2f})."
                )


def _render_player_combinations(raw_data_df):
    st.info("Here contains player information and combinations of statistics")
    num_players = st.radio("Number of players", [2, 3, 4, 5, 6], horizontal=True)

    player_combos = s.combination_league(raw_data_df, num_players)
    player_combos = player_combos.sort_values(by=["Points", "Team GD", "Goals"], ascending=False).reset_index(drop=True)
    player_combos = player_combos[
        ["Combination", "Avg_Rating", "Played", "Wins", "Draws", "Losses", "Points", "Win %", "Goals", "GPG", "Team GF", "Team GA", "Team GD"]
    ]

    st.toggle("Keep only unbeaten combinations", key="unbeaten_combinations")
    if st.session_state.unbeaten_combinations:
        player_combos = player_combos[player_combos["Win %"] == 1]
        st.write(f"There are {len(player_combos)} unbeaten combinations of {num_players} players")

    player_combos.insert(0, "Position", range(1, len(player_combos) + 1))
    st.dataframe(player_combos, hide_index=True)


def _render_charts_over_time(raw_data_df):
    st.info("Charts over time")
    st.title("Player Goals Bar Chart Race")

    animation_speed = st.slider("Animation speed (seconds)", 0.2, 2.0, 0.8, 0.1)
    restart = st.button("Restart animation")

    goal_race_df = raw_data_df.copy()
    goal_race_df = goal_race_df[goal_race_df["Name"] != "Ringer"].copy()
    goal_race_df["GW_Number"] = goal_race_df.groupby("Date").ngroup() + 1
    goal_race_df["GW"] = "GW" + goal_race_df["GW_Number"].astype(str)

    players = sorted(goal_race_df["Name"].unique().tolist())
    gameweek_totals = (
        goal_race_df.groupby(["GW_Number", "GW", "Name"], as_index=False)["Goals"]
        .sum()
        .sort_values(["GW_Number", "Name"])
    )

    if gameweek_totals.empty:
        return

    player_colors = {
        "Michael Dixon": "red",
        "James King": "blue",
        "Callum Goodyear": "green",
        "Daniel Hirst": "orange",
        "Jacob Stokes": "purple",
        "Steven Robinson": "yellow",
        "Jamie Dobbs": "black",
        "Oliver Deverall": "grey",
        "Rory Scullin": "silver",
        "Toby Munson": "purple",
        "Mark Mcglinchey": "teal",
    }

    max_goals = int(gameweek_totals.groupby("Name")["Goals"].sum().max())
    chart_placeholder = st.empty()
    cumulative_goals = {player: 0 for player in players}

    frame_sequence = [("Start", None)] + [
        (gw_label, gw_number)
        for gw_number, gw_label in (
            gameweek_totals[["GW_Number", "GW"]].drop_duplicates().sort_values("GW_Number").itertuples(index=False, name=None)
        )
    ]

    if restart:
        st.session_state["goal_race_restart_count"] = st.session_state.get("goal_race_restart_count", 0) + 1

    for gw_label, gw_number in frame_sequence:
        if gw_number is not None:
            gw_rows = gameweek_totals[gameweek_totals["GW_Number"] == gw_number]
            for row in gw_rows.itertuples(index=False):
                cumulative_goals[row.Name] += int(row.Goals)

        frame_df = _build_goal_race_frame(players, cumulative_goals)
        fig = px.bar(
            frame_df,
            x="TotalGoals",
            y="Player",
            orientation="h",
            text="TotalGoals",
            range_x=[0, max_goals + 1],
            color="Player",
            color_discrete_map=player_colors,
            height=400,
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"},
            title=f"Cumulative Goals up to {gw_label}",
            showlegend=False,
        )
        chart_placeholder.plotly_chart(fig, width="stretch")
        time.sleep(animation_speed)

    st.divider()
    st.title("Cumulative points over time")


def _build_goal_race_frame(players, cumulative_goals):
    frame_rows = [
        {"Player": player, "TotalGoals": cumulative_goals.get(player, 0)}
        for player in players
    ]
    return pd.DataFrame(frame_rows).sort_values(
        "TotalGoals",
        ascending=True,
    )


def _render_formation(raw_data_df):
    st.title("Gameweek Lineup – Team A vs Team B")

    df = raw_data_df.copy()
    df["GW"] = df.groupby("Date").ngroup() + 1

    positions_5_a = [(0.5, 0.08), (0.2, 0.28), (0.8, 0.28), (0.3, 0.42), (0.7, 0.42)]
    positions_5_b = [(0.5, 0.92), (0.2, 0.72), (0.8, 0.72), (0.3, 0.58), (0.7, 0.58)]
    positions_6_a = [(0.5, 0.08), (0.15, 0.28), (0.85, 0.28), (0.3, 0.42), (0.7, 0.42), (0.5, 0.30)]
    positions_6_b = [(0.5, 0.92), (0.15, 0.72), (0.85, 0.72), (0.3, 0.58), (0.7, 0.58), (0.5, 0.70)]

    gameweeks = {}
    for gw, gdf in df.groupby("GW"):
        team_a = gdf[gdf["Team"].str.startswith("A")]
        team_b = gdf[gdf["Team"].str.startswith("B")]
        motm = gdf[gdf["MOTM"] == gdf["MOTM"].max()]["Name"].tolist()
        gotg = gdf[gdf["GOTG"] == gdf["GOTG"].max()]["Name"].tolist()

        gameweeks[f"GW{gw}"] = {
            "team_a_name": f"GW{gw} Team A",
            "team_b_name": f"GW{gw} Team B",
            "motm": motm,
            "gotg": gotg,
            "team_a": _build_team_players(team_a, positions_6_a if len(team_a) == 6 else positions_5_a),
            "team_b": _build_team_players(team_b, positions_6_b if len(team_b) == 6 else positions_5_b),
        }

    f_c1, _ = st.columns([2, 7])
    with f_c1:
        gw = st.selectbox("Select Gameweek", list(gameweeks.keys()))

    data = gameweeks[gw]

    with urllib.request.urlopen(BALL_URL) as url:
        ball_img = plt.imread(BytesIO(url.read()))

    fig = _draw_pitch(data, ball_img)
    score_a = sum(player["goals"] for player in data["team_a"])
    score_b = sum(player["goals"] for player in data["team_b"])
    st.markdown(f"### {data['team_a_name']} {score_a} - {score_b} {data['team_b_name']}")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    st.image(buf, width=300)


def _build_team_players(team_df, positions):
    players = []
    for i, (_, row) in enumerate(team_df.iterrows()):
        players.append(
            {
                "name": row["Name"],
                "goals": int(row["Goals"]),
                "x": positions[i][0],
                "y": positions[i][1],
            }
        )
    return players


def _draw_pitch(data, ball_img, fig_scale=0.25):
    fig, ax = plt.subplots(figsize=(3.5 * fig_scale, 5 * fig_scale), dpi=150)
    ax.set_facecolor("#3f995b")

    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="white", lw=2 * fig_scale)
    ax.axhline(0.5, color="white", lw=1.5 * fig_scale)
    centre_circle = Circle((0.5, 0.5), 0.08, fill=False, color="white", lw=1.5 * fig_scale)
    ax.add_patch(centre_circle)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    def plot_team(players, color):
        for player in players:
            border_colors = []
            if player["name"] in data["motm"]:
                border_colors.append("gold")
            if player["name"] in data["gotg"]:
                border_colors.append("silver")

            for i, border_color in enumerate(border_colors):
                border = Circle(
                    (player["x"], player["y"]),
                    0.045 + 0.01 * (len(border_colors) - i - 1),
                    facecolor=color,
                    edgecolor=border_color,
                    linewidth=[3, 2][i] * fig_scale,
                )
                ax.add_patch(border)

            if not border_colors:
                border = Circle(
                    (player["x"], player["y"]),
                    0.045,
                    facecolor=color,
                    edgecolor="black",
                    linewidth=1.5 * fig_scale,
                )
                ax.add_patch(border)

            ax.text(
                player["x"],
                player["y"],
                player["name"],
                ha="center",
                va="center",
                fontsize=7 * fig_scale,
                color="white",
                weight="bold",
            )

            for i in range(player["goals"]):
                ab = AnnotationBbox(
                    OffsetImage(ball_img, zoom=0.02 * fig_scale),
                    (player["x"] - 0.03 + i * 0.035, player["y"] + 0.06),
                    frameon=False,
                )
                ax.add_artist(ab)

    plot_team(data["team_a"], "#d62828")
    plot_team(data["team_b"], "#1d4ed8")
    return fig

