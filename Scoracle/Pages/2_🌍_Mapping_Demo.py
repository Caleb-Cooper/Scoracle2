import streamlit as st
import pandas as pd
import pydeck as pdk
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

# Set Streamlit page configuration
st.set_page_config(page_title="NBA Team Travel Map 2023-2024", page_icon="🏀")

# Main title and description
st.title("NBA Team Travel Map 2023-2024")
st.sidebar.header("Select Team and Number of Games")
st.write("Visualize the travel path and game outcomes for NBA teams during the 2023-2024 season.")

# Define team location data
teams_data = {
    "team": ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", 
             "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", 
             "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", 
             "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", 
             "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", 
             "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", 
             "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", 
             "Utah Jazz", "Washington Wizards"],
    "latitude": [33.757289, 42.366198, 40.682646, 35.225195, 
                 41.880691, 41.496547, 32.790391, 39.748652, 
                 42.341103, 37.768018, 29.750921, 39.764043, 
                 34.043018, 34.043018, 35.138142, 25.781401, 
                 43.045080, 44.979463, 29.949035, 40.750505, 
                 35.463425, 28.539221, 39.901202, 33.445737, 
                 45.531565, 38.580205, 29.427020, 43.643466, 
                 40.768268, 38.898168],
    "longitude": [-84.396324, -71.062146, -73.975416, -80.839347, 
                  -87.674176, -81.688057, -96.810255, -105.007599, 
                  -83.055267, -122.387877, -95.362217, -86.155537, 
                  -118.267254, -118.267254, -90.050586, -80.186969, 
                  -87.917386, -93.276095, -90.082057, -73.993439, 
                  -97.515114, -81.383854, -75.171980, -112.071200, 
                  -122.666842, -121.499660, -98.437465, -79.379099, 
                  -111.901087, -77.020857]
}
teams_df = pd.DataFrame(teams_data)

# Fetch game data and merge with stadium coordinates
@st.cache_data
def fetch_game_data(team_id):
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable="2023-24")
    games = gamefinder.get_data_frames()[0]
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])
    games['home_game'] = games['MATCHUP'].str.contains('vs.')
    games['opponent'] = games['MATCHUP'].str.extract('(@|vs.) ([A-Z]{3})')[1]
    games = games.merge(teams_df, how='left', left_on='opponent', right_on='team')
    games.sort_values('GAME_DATE', inplace=True)
    return games

# User selections
team_ids = {team['full_name']: team['id'] for team in teams.get_teams()}
selected_team = st.sidebar.selectbox("Choose a team", list(team_ids.keys()))
num_games = st.sidebar.slider("Number of games to display", 1, 82, 10)

# Display map
if st.sidebar.button("Show Travel Map"):
    games_data = fetch_game_data(team_ids[selected_team]).head(num_games)
    if not games_data.empty:
        home_team_data = teams_df[teams_df['team'] == selected_team]
        if not home_team_data.empty:
            home_coords = home_team_data[['latitude', 'longitude']].values[0]
            away_games = games_data[games_data['home_game'] == False]
            points = away_games[['latitude', 'longitude']].dropna()
            
            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=points,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=20000,
                pickable=True
            )
            
            view_state = pdk.ViewState(latitude=home_coords[0], longitude=home_coords[1], zoom=5, pitch=50)
            
            st.pydeck_chart(pdk.Deck(
                layers=[scatter_layer],
                initial_view_state=view_state,
                map_style='mapbox://styles/mapbox/light-v9',
                tooltip={"text": "{latitude}, {longitude}"}
            ))
        else:
            st.error("No home coordinates available for the selected team.")
    else:
        st.error("No data available for the selected team and season.")
