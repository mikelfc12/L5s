import time
import uuid
import streamlit as st
import variables as v


# --- Helper functions ---
def show_center(names, center_box, highlight=None, drift=None):
    """Display remaining players in the center, with optional animation."""
    html = "<div style='text-align:center'>"
    for n in names:
        if n == highlight and drift:
            html += f"<div class='player {drift}'>{n}</div>"
        else:
            html += f"<div class='player'>{n}</div>"
    html += "</div>"
    center_box.markdown(html, unsafe_allow_html=True)


def update_teams(teamA_box, teamB_box, teamA, teamB):
    teamA_box.markdown("<br>".join(teamA) if teamA else "—", unsafe_allow_html=True)
    teamB_box.markdown("<br>".join(teamB) if teamB else "—", unsafe_allow_html=True)


def say(text,text_box, delay=4):
    """Animated text preamble."""
    existing = st.session_state.get("log", [])
    existing.append(text)
    st.session_state["log"] = existing
    text_box.markdown("<br>".join(existing), unsafe_allow_html=True)
    time.sleep(delay)


def clear_text_box(text_box):
    """Clear text box and reset log."""
    st.session_state["log"] = []
    text_box.empty()


def pick_work(a_or_b, pick, gif_box, remaining_players,teamA, teamB, teamA_box, teamB_box, caption_box):
    # caption_box.markdown(f"**{player_stats.get(pick, 'A true wildcard.')}**")
    time.sleep(1.5)

    gif_box.image(v.player_images.get(pick), width=300)
    time.sleep(3)

    show_center(remaining_players, highlight=pick, drift="left")
    if a_or_b == "A":
        teamA.append(pick)
    if a_or_b == "B":
        teamB.append(pick)
    update_teams(teamA_box,teamB_box, teamA, teamB)
    time.sleep(2)
    gif_box.empty()
    caption_box.empty()
    remaining_players.remove(pick)
    show_center(remaining_players)


def spin_image(
        image_path: str,
        container: st.empty,
        width: int = 300,
        spin_seconds: float = 6.0,
        pause_seconds: float = 3.0,
):
    # Load image
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    # Unique animation name (CRITICAL)
    anim_id = f"spinZoom_{uuid.uuid4().hex}"

    container.markdown(
        f"""
        <style>
        @keyframes {anim_id} {{
            0% {{
                transform: scale(0.2) rotate(0deg);
                opacity: 0;
            }}
            70% {{
                transform: scale(1.1) rotate(720deg);
                opacity: 1;
            }}
            100% {{
                transform: scale(1) rotate(0deg);
            }}
        }}

        .spin-image {{
            display: block;
            margin: 30px auto;
            width: {width}px;
            animation: {anim_id} {spin_seconds}s ease-out forwards;
        }}
        </style>

        <img src="data:image/png;base64,{img_base64}" class="spin-image">
        """,
        unsafe_allow_html=True,
    )

    # Hold on screen
    time.sleep(spin_seconds + pause_seconds)

    # Remove image
    container.empty()


def colour_negative_red(val):
    if isinstance(val, (int, float)) and val < 0:
        return "color: red;"
    return ""


def highlight_team_a(row):
    if str(row["Team"]).startswith("A"):
        return ["background-color: #f2f2f2"] * len(row)
    else:
        return [""] * len(row)

