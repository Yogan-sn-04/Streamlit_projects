import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Weather Wizard 🌦️", page_icon="🌦️", layout="wide")

# Inject Live Video Background
st.markdown(
    """
    <style>
    .video-bg {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        opacity: 0.4;
        object-fit: cover;
    }

    .stApp {
        background: transparent;
    }
    </style>

    <video autoplay muted loop class="video-bg">
        <source src="https://player.vimeo.com/external/357042091.sd.mp4?s=baf59e793514f740e1566f933d9cfe42456dc2b2&profile_id=139&oauth2_token_id=57447761" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# Load City + Country List
@st.cache_data
def load_city_country_pairs():
    try:
        df = pd.read_csv("worldcities.csv")
        df = df[['city', 'country']].dropna().drop_duplicates()
        df['label'] = df['city'] + ", " + df['country']
        return df.sort_values('label')
    except:
        return pd.DataFrame({'label': ["Delhi, India", "Mumbai, India", "New York, United States"]})

city_df = load_city_country_pairs()

# Weather condition media mapping
weather_media = {
    "Clear": {"icon": "☀️", "video": "https://www.youtube.com/embed/0_jNjpVxUt0"},
    "Clouds": {"icon": "☁️", "video": "https://www.youtube.com/embed/Jptq6mUa5IE"},
    "Rain": {"icon": "🌧️", "video": "https://www.youtube.com/embed/SnUBb-FAlCY"},
    "Drizzle": {"icon": "🌦️", "video": "https://www.youtube.com/embed/lSMVVLR9KIs"},
    "Thunderstorm": {"icon": "⛈️", "video": "https://www.youtube.com/embed/aPoXzzo2cSc"},
    "Snow": {"icon": "❄️", "video": "https://www.youtube.com/embed/7BrIJrjxVxA"},
    "Mist": {"icon": "🌫️", "video": "https://www.youtube.com/embed/w3PDyTWlStk"},
    "Default": {"icon": "🌈", "video": "https://www.youtube.com/embed/QVGwC-tywO4"}
}

# Error Handler
def show_error():
    st.error("💥 Weather server dodged our request like a ninja! Try again or check your city name.")

# Weather Fetcher
def get_weather(city, country, units="metric"):
    try:
        API_KEY = "4d8fb5b93d4af21d66a2948710284366"
        query = f"{city},{country}"
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units={units}"
        response = requests.get(URL)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Stylish Title
st.markdown("""
    <h1 style='text-align:center; color:#4B89DC; font-family: "Segoe UI", sans-serif;'>
        🧙‍♂️ Weather Wizard 🌦️
    </h1>
""", unsafe_allow_html=True)

st.write("Start typing your city and country:")

# City Selector with Country
city_label = st.selectbox(
    "📍 Choose your location (City, Country)",
    options=city_df['label'].tolist(),
    index=city_df['label'].tolist().index("Delhi, India") if "Delhi, India" in city_df['label'].tolist() else 0
)

# Extract city and country for query
city_row = city_df[city_df['label'] == city_label].iloc[0]
selected_city = city_row['city']
selected_country = city_row['country']

# Get Weather Button
if st.button("🔍 Get Forecast"):
    data = get_weather(selected_city, selected_country)

    if data:
        weather_main = data['weather'][0]['main']
        weather_desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        media = weather_media.get(weather_main, weather_media["Default"])

        # Layout
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"<h2 style='color:#f39c12;'>{media['icon']} Weather in <strong>{selected_city.title()}, {selected_country}</strong></h2>", unsafe_allow_html=True)
            st.write(f"**Condition:** {weather_desc}")
            st.write(f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)")
            st.write(f"💧 Humidity: {humidity}%")
            st.write(f"💨 Wind Speed: {wind_speed} m/s")

        with col2:
            st.markdown("### Weather vibes 🎥")
            st.markdown(f"""
                <div style="position: relative; width: 100%; max-width: 600px; padding-top: 50%;">
                    <iframe src="{media['video']}?autoplay=1&start=5&mute=1"
                            frameborder="0"
                            allow="autoplay; encrypted-media"
                            allowfullscreen
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                    </iframe>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("🌍 Powered by OpenWeatherMap & curated weather videos 🎬")
    else:
        show_error()
