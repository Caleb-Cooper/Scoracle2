import streamlit as st
import numpy as np
import streamlit as st
import random
from collections import Counter
from itertools import combinations, cycle
from math import comb

# Function to navigate to different pages
def navigate_to_page(page):
    if page == "Plotting Demo":
        st.components.v1.iframe("pages/1_📈_Plotting_Demo.py")
    elif page == "Mapping Demo":
        st.components.v1.iframe("pages/2_🌍_Mapping_Demo.py")
    elif page == "DataFrame Demo":
        st.components.v1.iframe("pages/3_📊_DataFrame_Demo.py")
    elif page == "Team Locations":
        st.components.v1.iframe("team_locations.py")
    elif page == "Scoracle":
        st.components.v1.iframe("Scoracle.py")

# Set page configuration
st.set_page_config(
    page_title="Scoracle",
    page_icon="🔮",
    layout="centered"
)

# Home page content
st.markdown("# Welcome to Scoracle! 🔮")

# Function to simulate random scores based on given scores for two teams
def simulate_scores(team1_scores, team2_scores, simulations=10000):
    return [(random.choice(team1_scores), random.choice(team2_scores)) for _ in range(simulations)]

# Function to calculate basic statistics from simulated scores
def calculate_statistics(simulated_scores):
    total_scores = [sum(scores) for scores in simulated_scores]
    avg_score = sum(total_scores) / len(total_scores)
    highest_score = max(total_scores)
    lowest_score = min(total_scores)
    score_freq = Counter(total_scores)
    most_common_score_total, occurrences = score_freq.most_common(1)[0]
    return avg_score, highest_score, lowest_score, total_scores, (most_common_score_total, occurrences)

# Function to analyze how many scores went over or under given thresholds
def analyze_over_under(total_scores, overs, unders):
    results = {}
    for over in overs:
        over_count = sum(score > over for score in total_scores)
        over_percentage = (over_count / len(total_scores)) * 100
        results[f'over {over}'] = (over_count, over_percentage)
    for under in unders:
        under_count = sum(score < under for score in total_scores)
        under_percentage = (under_count / len(total_scores)) * 100
        results[f'under {under}'] = (under_count, under_percentage)
    return results

# Function to generate evenly distributed parlays from a list of events
def generate_evenly_distributed_parlays(events):
    parlays = []
    event_count = len(events)
    total_parlays = comb(event_count, 2)
    event_cycle = cycle(events)
    used_pairs = set()  # This will store tuples instead of sets
    
    while len(parlays) < total_parlays:
        for i in range(event_count):
            base_event = next(event_cycle)
            for j in range(1, event_count):
                pairing_event = events[(i + j) % event_count]
                if (base_event, pairing_event) not in used_pairs and (pairing_event, base_event) not in used_pairs:
                    parlays.append((base_event, pairing_event))
                    used_pairs.add((base_event, pairing_event))  # Store as a tuple
                    if len(parlays) == total_parlays:
                        break
            if len(parlays) == total_parlays:
                break
    return parlays


# Main application layout and logic
st.title('Sports Score Simulation & 2-Bet Parlay')

tab1, tab2 = st.tabs(["Score Simulation", "2-Bet Parlay"])

with tab1:
    # List of NBA teams
    nba_teams = [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
        "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors",
        "Houston Rockets", "Indiana Pacers", "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies",
        "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
        "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
        "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"
    ]

with tab1:
    st.subheader("Team Selection")
    col1, col2 = st.columns(2)
    with col1:
        team1_name = st.selectbox("Select the first team:", nba_teams, key='team1_name')
        team1_scores = st.text_input("Enter the scores for team 1 separated by space:", key='team1_scores')
    with col2:
        team2_name = st.selectbox("Select the second team:", nba_teams, key='team2_name')
        team2_scores = st.text_input("Enter the scores for team 2 separated by space:", key='team2_scores')

    st.subheader("Options")
    col1, col2 = st.columns(2)
    with col1:
        overs = [
            st.number_input("Enter first 'over' value (optional):", step=1, key='over1'),
            st.number_input("Enter second 'over' value (optional):", step=1, key='over2')
        ]
    with col2:
        unders = [
            st.number_input("Enter first 'under' value (optional):", step=1, key='under1'),
            st.number_input("Enter second 'under' value (optional):", step=1, key='under2')
        ]

    if st.button('Simulate and Analyze', key='analyze_simulation'):
        if team1_scores and team2_scores:
            try:
                team1_scores = list(map(int, team1_scores.split()))
                team2_scores = list(map(int, team2_scores.split()))
                with st.spinner('Running simulation...'):
                    simulated_scores = simulate_scores(team1_scores, team2_scores)
                    avg_score, highest_score, lowest_score, total_scores, most_common_score_total = calculate_statistics(simulated_scores)
                    st.success("Simulation completed!")

                st.write(f"Average Total Score: {avg_score:.2f}")
                st.write(f"Highest Score: {highest_score}")
                st.write(f"Lowest Score: {lowest_score}")
                st.write(f"Most Likely Total Score: {most_common_score_total[0]} occurring {most_common_score_total[1]} times")

                overs = [over for over in overs if over > 0]
                unders = [under for under in unders if under > 0]

                results = analyze_over_under(total_scores, overs, unders)
                for key, (count, percentage) in results.items():
                    st.write(f"- Final score went {key} {count} times ({percentage:.2f}% of the time).")
            except ValueError:
                st.error("Please enter valid integers for scores.")


with tab2:
    st.subheader("2-Bet Parlay Generator")
    
    if 'event_count' not in st.session_state:
        st.session_state.event_count = 2
    
    def add_event():
        if st.session_state.event_count < 10:
            st.session_state.event_count += 1

    def remove_event():
        if st.session_state.event_count > 2:
            st.session_state.event_count -= 1

    events = []
    for i in range(st.session_state.event_count):
        event = st.text_input(f"Enter game event {i+1}:", key=f'parlay_event{i+1}')
        if event:
            events.append(event)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Add Event", on_click=add_event)

    with col2:
        st.button("Remove Event", on_click=remove_event)

    if st.button('Generate Evenly Distributed Parlays', key='generate_even_parlays'):
        if len(events) >= 2:
            parlays = generate_evenly_distributed_parlays(events)
            parlay_text = f"Generated {len(parlays)} evenly distributed 2-bet parlays:\n\n"
            parlay_details = "\n".join([f"{i+1}. {par[0]} / {par[1]}" for i, par in enumerate(parlays)])
            parlay_text += parlay_details
            st.success(f"Generated {len(parlays)} evenly distributed 2-bet parlays:")
            st.text(parlay_text)

            # Create a download button
            st.download_button(
                label="Download Parlays",
                data=parlay_text,
                file_name="2_bet_parlays.txt",
                mime='text/plain'
            )
        else:
            st.error("Please enter at least 2 game events to generate parlays.")

