import streamlit as st
import pandas as pd
import altair as alt
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog

st.set_page_config(page_title="NBA Team Points Comparison", page_icon="🏀")

st.markdown("# NBA Team Points Comparison")
st.sidebar.header("NBA Team Points Comparison")
st.write(
    """This app allows users to compare NBA teams based on total points scored over their last 9 games."""
)

# Fetch team data using st.cache_data for improved performance and up-to-date caching
@st.cache_data
def load_teams():
    nba_teams = teams.get_teams()
    return {team['full_name']: team['id'] for team in nba_teams}

team_name_to_id = load_teams()

# Use st.cache_data to cache game log data
@st.cache_data
def fetch_data(team_id):
    game_log = teamgamelog.TeamGameLog(team_id=team_id, season='2023-24')
    df = game_log.get_data_frames()[0]
    return df.head(9)  # We only need the last 9 games

try:
    team_names = st.multiselect("Choose teams", list(team_name_to_id.keys()), ["Atlanta Hawks"])
    if not team_names:
        st.error("Please select at least one team.")
    else:
        frames = []
        for team_name in team_names:
            team_id = team_name_to_id[team_name]
            df = fetch_data(team_id)
            df['Game_Number'] = range(1, len(df) + 1)  # Number games from 1 to 9
            frames.append(df[['Game_Number', 'PTS']].assign(Team_Name=team_name))

        combined_df = pd.concat(frames)
        st.write("### Points Scored in the Last 9 Games", combined_df)

        chart = (
            alt.Chart(combined_df)
            .mark_line(point=True)
            .encode(
                x='Game_Number:N',
                y='PTS:Q',
                color='Team_Name:N',
                tooltip=['Game_Number', 'PTS', 'Team_Name']
            )
            .properties(
                title='NBA Team Comparison: Points Scored in Last 9 Games'
            )
        )
        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {e}")
