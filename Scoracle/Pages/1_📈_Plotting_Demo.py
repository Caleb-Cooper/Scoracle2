import streamlit as st
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
import time

# Set Streamlit page configuration
st.set_page_config(page_title="NBA Season Trend", page_icon="📈")

# Main title and description
st.markdown("# NBA Season Trend")
st.sidebar.header("NBA Season Trend")
st.write("This demo allows you to select NBA teams and visualize their scoring trends over the current season.")

# Function to load teams
@st.cache_data
def load_teams():
    nba_teams = teams.get_teams()
    return {team['full_name']: team['id'] for team in nba_teams}

# Function to fetch game data
@st.cache_data
def fetch_game_data(team_id, season="2023-24"):
    game_log = teamgamelog.TeamGameLog(team_id=team_id, season=season)
    df = game_log.get_data_frames()[0]
    df['PTS'] = pd.to_numeric(df['PTS'])
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])  # Ensure GAME_DATE is in datetime format
    return df[['GAME_DATE', 'PTS']]

# Load teams data
team_name_to_id = load_teams()
selected_teams = st.sidebar.multiselect("Choose teams", list(team_name_to_id.keys()))

if selected_teams:
    combined_data = pd.DataFrame()

    for team_name in selected_teams:
        team_id = team_name_to_id[team_name]
        game_data = fetch_game_data(team_id)
        game_data['Team'] = team_name
        combined_data = pd.concat([combined_data, game_data], ignore_index=True)

    # Sort combined_data by 'GAME_DATE' to ensure chronological order
    combined_data.sort_values('GAME_DATE', inplace=True)

    chart_placeholder = st.empty()  # Placeholder for the animated chart

    # Animation loop
    unique_dates = combined_data['GAME_DATE'].unique()
    for date_index in range(1, len(unique_dates) + 1):
        # Filter data up to the current date in the loop
        subset_data = combined_data[combined_data['GAME_DATE'].isin(unique_dates[:date_index])]
        pivoted_subset = subset_data.pivot_table(index='GAME_DATE', columns='Team', values='PTS', aggfunc='sum')

        # Update the chart placeholder with new data
        chart_placeholder.line_chart(pivoted_subset, use_container_width=True)

        # Add delay for animation
        time.sleep(0.1)  # Adjust sleep time for animation speed

# Add a re-run button for convenience
st.button("Re-run")
