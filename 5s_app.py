import streamlit as st
import time

import pandas as pd
import bar_chart_race as bcr
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import urllib.request
from io import BytesIO

ball_url = "https://assets.streamlinehq.com/image/private/w_512,h_512,ar_1/f_auto/v1/icons/7/soccer-ball-gapr651upnuseroqnw7ppl.png/soccer-ball-gsnnt0o2y4wtvehff0ckg.png?_a=DATAiZAAZAA0"

import variables as v
import statistics as s
import functions as func
import display_functions as disp_f

# # TEAM INFORMATION
team_A_starter = ["Mark McGlinchey", "Daniel Hirst", "Kevin"]
team_B_starter = ["Rory Scullin", "Steven Robinson", "Callum Goodyear", "Jacob Stokes"]
pot_1 = ["Michael Dixon", "Jamie Dobbs", "James King"]

team_A, team_B = func.generate_teams(pot_1, team_A_starter, team_B_starter, v.previous_teams)

print("Team A:", team_A)
print("Team B:", team_B)

# --- Page setup ---
st.set_page_config(page_title="4MOST 5-a-Side Draw", layout="wide")
st.title("⚽ The Official 4MOST 5-a-Side Draw ⚽")

##################### SESSION STATE VARIABLES
if "rpt" not in st.session_state:
    st.session_state.rpt = False
if "unbeaten_combinations" not in st.session_state:
    st.session_state.unbeaten_combinations = False

# --- CSS animations ---
st.markdown("""
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
""", unsafe_allow_html=True)

draw_tab, stats_tab = st.tabs(["Draw", "Statistics"])

with draw_tab:
    # --- Layout ---
    col1, col2, col3 = st.columns([3, 2, 3])
    with col1:
        st.markdown("### 🟥 Team A")
        teamA_box = st.empty()
    with col2:
        text_box = st.empty()
        gif_box = st.empty()
        spinning_card_slot = st.empty()
        caption_box = st.empty()
        center_box = st.empty()

    with col3:
        st.markdown("### 🟦 Team B")
        teamB_box = st.empty()

    teamA, teamB = [], []

    # --- Start draw ---
    if st.button("🎬 Begin the Show!"):
        st.session_state["log"] = []

        disp_f.say("Welcome to the **4MOST 5-a-Side Draw**", text_box)

        disp_f.say("Speaking of which, lets have a weather report", text_box)
        gif_box.image("x.png")
        time.sleep(5)
        gif_box.empty()

        disp_f.say("We go again with the 10% chance of rain glitch", text_box)

        disp_f.clear_text_box(text_box)
        text_box.empty()

        disp_f.say("Right, lets get into the draw...", text_box)

        disp_f.clear_text_box(text_box)
        text_box.empty()

        # Draw sequence begins
        remaining_players = team_A + team_B
        disp_f.show_center(remaining_players, center_box)

        fixed_teamA = []
        fixed_teamB = []

        # Alternate picks
        for a_player, b_player in zip(team_A, team_B):
            # TEAM A
            disp_f.pick_work("A", a_player, gif_box, remaining_players, teamA, teamB, teamA_box, teamB_box, caption_box)
            time.sleep(5)
            fixed_teamA.append(a_player)

            # TEAM B
            disp_f.pick_work("B", b_player, gif_box, remaining_players, teamA, teamB, teamA_box, teamB_box, caption_box)
            time.sleep(5)
            fixed_teamB.append(b_player)

        disp_f.say("Some stats on these teams please, if any", text_box)

        # Check team A
        never_A = func.check_pairs(team_A, v.never_won_pairs)
        perfect_A = func.check_pairs(team_A, v.perfect_record_pairs)
        never_played_A = func.check_pairs(team_A, v.never_played_pairs)

        # Check team B
        never_B = func.check_pairs(team_B, v.never_won_pairs)
        perfect_B = func.check_pairs(team_B, v.perfect_record_pairs)
        never_played_B = func.check_pairs(team_B, v.never_played_pairs)

        st.markdown("### Team A Alerts")

        if never_played_A:
            for p1, p2 in never_played_A:
                st.warning(f"{p1} & {p2} have never played together")

        if never_A:
            for p1, p2 in never_A:
                st.error(f"❌ {p1} & {p2} have NEVER won together")

        if perfect_A:
            for p1, p2 in perfect_A:
                st.success(f"🔥 {p1} & {p2} have a 100% record together")

        if not never_A and not perfect_A and not never_played_A:
            st.info("No special pair alerts for Team A")

        st.markdown("### Team B Alerts")

        if never_played_B:
            for p1, p2 in never_played_B:
                st.warning(f"{p1} & {p2} have never played together")

        if never_B:
            for p1, p2 in never_B:
                st.error(f"❌ {p1} & {p2} have NEVER won together")

        if perfect_B:
            for p1, p2 in perfect_B:
                st.success(f"🔥 {p1} & {p2} have a 100% record together")

        if not never_B and not perfect_B and not never_played_B:
            st.info("No special pair alerts for Team B")

        st.success("🏁 The draw is complete!")
        st.balloons()

with stats_tab:
    st.info("Stats")
    league_table, latest_match, player_combinations, charts_over_time, formation, raw_data = st.tabs(
        ["League Table", "Last match", "Player Combinations", "Charts over time", "Formations", "View Raw Data"])
    with league_table:

        raw_data_df = pd.read_csv("raw_data.csv")
        player_table = s.convert_to_player_table(raw_data_df)

        two_dp_cols = ["Avg_Rating", "GPG", "Ave TGF", "Ave TGA", "Ave TGD", "Ave MOTM", "Ave GOTG"]
        percent_cols = ["Win %", "% of team goals", "% of total goals"]

        format_dict = {
            **{col: "{:.2f}" for col in two_dp_cols},
            **{col: "{:.1%}" for col in percent_cols},
        }

        st.toggle("Remove part timers", key="rpt")
        table = player_table.copy()
        if st.session_state.rpt:
            player_table_3plus = table[(table['Played'] >= 3) & (table['Name'] != "Ringer")].copy()
            player_table_under3 = table[(table['Played'] < 3) | (table['Name'] == "Ringer")].copy()

            player_table_3plus["Position"] = range(1, len(player_table_3plus) + 1)
            player_table_under3["Position"] = range(1, len(player_table_under3) + 1)

            # Players who haven't played 3 games
            styled_p3 = (player_table_3plus.style.format(format_dict)
                         .set_properties(subset=["Played", "Wins", "Draws", "Losses", "Points", "Win %"],
                                         **{"background-color": "#f8d7da"})
                         .set_properties(subset=['Goals', 'GPG', '% of team goals', '% of total goals'],
                                         **{"background-color": "#7bf542"})
                         .set_properties(subset=['Team_GF', 'Team_GA', 'Team_GD', 'Ave TGF', 'Ave TGA', 'Ave TGD', ],
                                         **{"background-color": "#f5cb42"})
                         .set_properties(subset=['MOTM', 'Ave MOTM', 'GOTG', 'Ave GOTG'],
                                         **{"background-color": "#f0faa2"})
                         .map(disp_f.colour_negative_red)
                         )
            styled_u3 = (player_table_under3.style.format(format_dict)
                         .set_properties(subset=["Played", "Wins", "Draws", "Losses", "Points", "Win %"],
                                         **{"background-color": "#f8d7da"})
                         .set_properties(subset=['Goals', 'GPG', '% of team goals', '% of total goals'],
                                         **{"background-color": "#7bf542"})
                         .set_properties(subset=['Team_GF', 'Team_GA', 'Team_GD', 'Ave TGF', 'Ave TGA', 'Ave TGD', ],
                                         **{"background-color": "#f5cb42"})
                         .set_properties(subset=['MOTM', 'Ave MOTM', 'GOTG', 'Ave GOTG'],
                                         **{"background-color": "#f0faa2"})
                         .map(disp_f.colour_negative_red)
                         )
            st.dataframe(styled_p3, hide_index=True)
            st.divider()
            st.dataframe(styled_u3, hide_index=True)
        else:
            all_players = table.copy()
            all_players["Position"] = range(1, len(all_players) + 1)

            styled = (all_players.style.format(format_dict)
                      .set_properties(subset=["Played", "Wins", "Draws", "Losses", "Points", "Win %"],
                                      **{"background-color": "#f8d7da"})
                      .set_properties(subset=['Goals', 'GPG', '% of team goals', '% of total goals'],
                                      **{"background-color": "#7bf542"})
                      .set_properties(subset=['Team_GF', 'Team_GA', 'Team_GD', 'Ave TGF', 'Ave TGA', 'Ave TGD', ],
                                      **{"background-color": "#f5cb42"})
                      .set_properties(subset=['MOTM', 'Ave MOTM', 'GOTG', 'Ave GOTG'],
                                      **{"background-color": "#f0faa2"})
                      .map(disp_f.colour_negative_red)
                      )

            st.dataframe(styled, hide_index=True)

    with latest_match:
        col1, col2 = st.columns([1, 1])
        with col1:
            last_match_stats = s.last_game_stats(raw_data_df)

            styled = (last_match_stats.style.format({"Rating": "{:.2f}", "MOTM": "{:.0f}", "GOTG": "{:.0f}"}).apply(
                disp_f.highlight_team_a, axis=1))

            st.dataframe(styled, hide_index=True)
        with col2:
            st.markdown("### Information about any key ratings")
            buffer_average = st.radio("Select % within for average", [1, 2.5, 5, 7.5, 10, ], horizontal=True)

            # Max rating, Min rating, Within 5% of average rating
            aggregated_df = (raw_data_df.groupby("Name").agg(
                Max_R=("Rating", "max"),
                Min_R=("Rating", "min"),
                Mean_R=("Rating", "mean")
            ).reset_index())
            summary_df = aggregated_df.merge(last_match_stats, on="Name", how="left")

            for _, row in summary_df.iterrows():
                player_name = row["Name"]

                latest = row["Rating"]
                max_r = row["Max_R"]
                min_r = row["Min_R"]
                mean_r = row["Mean_R"]

                gap = buffer_average / 100
                within_pct = abs(latest - mean_r) <= gap * mean_r

                if latest == max_r:
                    st.success(f"ℹ️ {player_name} recorded their highest rating ({latest:.2f}).")

                elif latest == min_r:
                    st.error(f"ℹ️ {player_name} recorded their lowest rating ({latest:.2f}).")

                elif within_pct:
                    st.warning(
                        f"ℹ️ {player_name}'s latest rating ({latest:.2f}) is within {gap * 100}% of their average ({mean_r:.2f}).")

    with player_combinations:
        st.info("Here contains player information and combinations of statistics")
        num_players = st.radio("Number of players", [2, 3, 4, 5, 6], horizontal=True)

        player_combinations = s.combination_league(raw_data_df, num_players)

        player_combinations = player_combinations.sort_values(by=["Points", "Team GD", "Goals"],
                                                              ascending=False).reset_index(drop=True)

        player_combinations = player_combinations[
            ['Combination', 'Avg_Rating', 'Played', 'Wins', 'Draws', 'Losses', 'Points', 'Win %',
             'Goals', 'GPG', 'Team GF', 'Team GA', 'Team GD']]

        # '% of team goals', '% of total goals',

        st.toggle("Keep only unbeaten combinations", key="unbeaten_combinations")

        if st.session_state.unbeaten_combinations:
            player_combinations = player_combinations[player_combinations["Win %"] == 1]

            st.write(f"There are {len(player_combinations)} unbeaten combinations of {num_players} players")

        player_combinations.insert(0, "Position", range(1, len(player_combinations) + 1))

        st.dataframe(player_combinations, hide_index=True)

        with charts_over_time:
            st.info("Charts over time")

            # View as of

            # Total view over time

            # Select player comparison

            # Select graphic

            # Goals per GOTG

            # Display the chart as it moves through the game weeks - show goals to start

            # Sample data: rows = players, columns = gameweeks
            # do this by minute of the game - chunk up goals and split by like 1/4 round and net adjust

            st.title("Player Goals Bar Chart Race")
            if st.button("Restart animation"):
                current_loop = 0

            # Manipulate raw_data into format required
            goal_race_df = raw_data_df.rename(columns={"Name": "Player"})
            goal_race_df = goal_race_df[goal_race_df['Player'] != "Ringer"]

            goal_race_df['GW'] = goal_race_df['Team'].str.replace("A", "GW")
            goal_race_df['GW'] = goal_race_df['GW'].str.replace("B", "GW")

            goal_race_df = goal_race_df[["Player", "GW", "Goals"]]

            goal_race_df = goal_race_df.pivot(index='Player', columns="GW", values="Goals").fillna(0).reset_index()

            gameweeks = [col for col in goal_race_df.columns if col != 'Player']

            player_colors = {
                'Michael Dixon': 'red',
                'James King': 'blue',
                'Callum Goodyear': 'green',
                'Daniel Hirst': 'orange',
                'Jacob Stokes': 'purple',
                'Steven Robinson': 'yellow',
                'Jamie Dobbs': 'black',
                'Oliver Deverall': 'grey',
                'Rory Scullin': 'silver',
                'Toby Munson': 'purple',
                'Mark Mcglinchey': 'teal',
            }

            # Placeholder for the chart
            chart_placeholder = st.empty()

            # Loop forever
            chart_id = 0
            max_loops = 1
            current_loop = 0
            gw_index = 0

            # TODO: FRAGMENT
            while current_loop < max_loops:
                gw = gameweeks[gw_index]
                chart_id += 1

                # Calculate cumulative goals up to this gameweek
                goal_race_df['TotalGoals'] = goal_race_df[gameweeks[:gw_index + 1]].sum(axis=1)
                df_sorted = goal_race_df.sort_values('TotalGoals', ascending=True)

                # Create horizontal bar chart
                fig = px.bar(
                    df_sorted,
                    x='TotalGoals',
                    y='Player',
                    orientation='h',
                    text='TotalGoals',
                    range_x=[0, goal_race_df['TotalGoals'].max() + 5],
                    color='Player',
                    color_discrete_map=player_colors,
                    height=400
                )

                fig.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    title=f"Cumulative Goals up to {gw}",
                    showlegend=False
                )

                chart_placeholder.plotly_chart(fig, width='stretch', key=f"chart_{chart_id}")

                # Move to next gameweek
                gw_index = (gw_index + 1)

                if gw_index >= len(gameweeks):
                    gw_index = 0
                    current_loop += 1  # count completed cycle

                # Pause for animation speed
                # time.sleep(2)
                st

        with formation:

            st.title("Gameweek Lineup – Team A vs Team B")

            gameweeks = {
                "GW1": {
                    "team_a_name": "GW1 Warriors",
                    "team_b_name": "GW1 Titans",
                    "motm": ["Jacob Stokes", "Michael Dixon"],
                    "gotg": ["Jacob Stokes"],
                    "team_a": [
                        {"name": "Michael Dixon", "goals": 2, "x": 0.5, "y": 0.08},
                        {"name": "James King", "goals": 1, "x": 0.2, "y": 0.28},
                        {"name": "Callum Goodyear", "goals": 0, "x": 0.8, "y": 0.28},
                        {"name": "Daniel Hirst", "goals": 1, "x": 0.3, "y": 0.42},
                        {"name": "Jacob Stokes", "goals": 3, "x": 0.7, "y": 0.42},
                    ],
                    "team_b": [
                        {"name": "Player B1", "goals": 1, "x": 0.5, "y": 0.92},
                        {"name": "Player B2", "goals": 0, "x": 0.2, "y": 0.72},
                        {"name": "Player B3", "goals": 2, "x": 0.8, "y": 0.72},
                        {"name": "Player B4", "goals": 0, "x": 0.3, "y": 0.58},
                        {"name": "Player B5", "goals": 1, "x": 0.7, "y": 0.58},
                    ],
                },
                "GW2": {
                    "team_a_name": "Red GW2",
                    "team_b_name": "Blue GW2",
                    "motm": ["Jacob Stokes", "Michael Dixon"],
                    "gotg": ["Daniel Hirst", "Player B3"],
                    "team_a": [
                        {"name": "Michael Dixon", "goals": 8, "x": 0.5, "y": 0.08},
                        {"name": "James King", "goals": 1, "x": 0.2, "y": 0.28},
                        {"name": "Callum Goodyear", "goals": 0, "x": 0.8, "y": 0.28},
                        {"name": "Daniel Hirst", "goals": 1, "x": 0.3, "y": 0.42},
                        {"name": "Jacob Stokes", "goals": 3, "x": 0.7, "y": 0.42},
                    ],
                    "team_b": [
                        {"name": "Player B1", "goals": 1, "x": 0.5, "y": 0.92},
                        {"name": "Player B2", "goals": 0, "x": 0.2, "y": 0.72},
                        {"name": "Player B3", "goals": 2, "x": 0.8, "y": 0.72},
                        {"name": "Player B4", "goals": 0, "x": 0.3, "y": 0.58},
                        {"name": "Player B5", "goals": 1, "x": 0.7, "y": 0.58},
                    ],
                }
            }

            gw = st.selectbox("Select Gameweek", list(gameweeks.keys()))
            data = gameweeks[gw]

            with urllib.request.urlopen(ball_url) as url:
                ball_img = plt.imread(BytesIO(url.read()))


            def draw_pitch(data, fig_scale=0.25):
                # fig_scale = fraction of original size
                fig, ax = plt.subplots(figsize=(3.5 * fig_scale, 5 * fig_scale), dpi=150)
                ax.set_facecolor("#3f995b")

                # Pitch boundary
                ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="white", lw=2 * fig_scale)
                ax.axhline(0.5, color="white", lw=1.5 * fig_scale)
                centre_circle = Circle((0.5, 0.5), 0.08, fill=False, color="white", lw=1.5 * fig_scale)
                ax.add_patch(centre_circle)

                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)

                motm_list = data["motm"]
                gotg_list = data["gotg"]

                radius = 0.045
                border_widths = [3, 2]

                def plot_team(players, color):
                    for player in players:
                        # Determine border order: gold outside, silver inside
                        border_colors = []
                        if player["name"] in motm_list:
                            border_colors.append("gold")
                        if player["name"] in gotg_list:
                            border_colors.append("silver")

                        # Draw borders
                        for i, bcolor in enumerate(border_colors):
                            border = Circle(
                                (player["x"], player["y"]),
                                radius + 0.01 * (len(border_colors) - i - 1),
                                facecolor=color,
                                edgecolor=bcolor,
                                linewidth=border_widths[i] * fig_scale
                            )
                            ax.add_patch(border)
                        if not border_colors:
                            border = Circle(
                                (player["x"], player["y"]),
                                radius,
                                facecolor=color,
                                edgecolor="black",
                                linewidth=1.5 * fig_scale
                            )
                            ax.add_patch(border)

                        # Full name
                        ax.text(player["x"], player["y"], player["name"],
                                ha="center", va="center",
                                fontsize=7 * fig_scale, color="white", weight="bold")

                        # Horizontal footballs below name
                        for i in range(player["goals"]):
                            ab = AnnotationBbox(
                                OffsetImage(ball_img, zoom=0.02 * fig_scale),
                                (player["x"] - 0.03 + i * 0.035, player["y"] + 0.06),
                                frameon=False
                            )
                            ax.add_artist(ab)

                plot_team(data["team_a"], "#d62828")
                plot_team(data["team_b"], "#1d4ed8")

                return fig


            score_a = sum(p["goals"] for p in data["team_a"])
            score_b = sum(p["goals"] for p in data["team_b"])
            st.markdown(f"### {data['team_a_name']} {score_a} - {score_b} {data['team_b_name']}")

            # Draw high-res figure
            fig = draw_pitch(data)

            # Save to buffer and display scaled down
            import io

            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)
            st.image(buf, width=300)  # width=300 scales it down in Streamlit without losing sharpness

            # fig = draw_pitch(data, fig_scale=1)
            # st.pyplot(fig, clear_figure=True)

        with raw_data:
            raw_data_df
