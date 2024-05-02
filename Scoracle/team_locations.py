import pandas as pd

# Create a DataFrame from the provided location data
teams_data = {
    "team": [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", 
        "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", 
        "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", 
        "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", 
        "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", 
        "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", 
        "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", 
        "Utah Jazz", "Washington Wizards"
    ],
    "location": [
        "State Farm Arena, Atlanta, Georgia", "TD Garden, Boston, Massachusetts", 
        "Barclays Center, Brooklyn, New York", "Spectrum Center, Charlotte, North Carolina", 
        "United Center, Chicago, Illinois", "Rocket Mortgage FieldHouse, Cleveland, Ohio", 
        "American Airlines Center, Dallas, Texas", "Ball Arena, Denver, Colorado", 
        "Little Caesars Arena, Detroit, Michigan", "Chase Center, San Francisco, California", 
        "Toyota Center, Houston, Texas", "Gainbridge Fieldhouse, Indianapolis, Indiana", 
        "Crypto.com Arena, Los Angeles, California", "Crypto.com Arena, Los Angeles, California", 
        "FedExForum, Memphis, Tennessee", "FTX Arena, Miami, Florida", 
        "Fiserv Forum, Milwaukee, Wisconsin", "Target Center, Minneapolis, Minnesota", 
        "Smoothie King Center, New Orleans, Louisiana", "Madison Square Garden, New York, New York", 
        "Paycom Center, Oklahoma City, Oklahoma", "Amway Center, Orlando, Florida", 
        "Wells Fargo Center, Philadelphia, Pennsylvania", "Footprint Center, Phoenix, Arizona", 
        "Moda Center, Portland, Oregon", "Golden 1 Center, Sacramento, California", 
        "AT&T Center, San Antonio, Texas", "Scotiabank Arena, Toronto, Ontario", 
        "Vivint Arena, Salt Lake City, Utah", "Capital One Arena, Washington, D.C."
    ],
    "latitude": [
        33.7572891, 42.366198, 40.6826465, 35.2251952, 
        41.8806908, 41.4965474, 32.7903908, 39.7486519, 
        42.3411026, 37.7680183, 29.7509213, 39.7640434, 
        34.0430175, 34.0430175, 35.1381418, 25.7814014, 
        43.0450802, 44.9794633, 29.9490351, 40.7505045, 
        35.4634247, 28.5392214, 39.9012015, 33.445737, 
        45.5315651, 38.5802045, 29.4270201, 43.6434661, 
        40.7682681, 38.8981675
    ],
    "longitude": [
        -84.3963244, -71.062146, -73.9754156, -80.8393468, 
        -87.6741759, -81.6880574, -96.8102547, -105.0075988, 
        -83.0552673, -122.3878772, -95.3622173, -86.1555367, 
        -118.2672541, -118.2672541, -90.0505864, -80.186969, 
        -87.9173862, -93.2760947, -90.0820568, -73.9934387, 
        -97.5151138, -81.3838535, -75.1719795, -112.0712003, 
        -122.6668423, -121.4996602, -98.4374652, -79.3790989, 
        -111.9010874, -77.0208568
    ]
}

teams_df = pd.DataFrame(teams_data)
