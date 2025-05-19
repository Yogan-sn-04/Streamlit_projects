import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Weather Wizard 🌦️", page_icon="🌦️", layout="wide")

# Load City List
@st.cache_data
def load_cities():
    try:
        df = pd.read_csv("worldcities.csv")
        return sorted(df['city'].dropna().unique().tolist())
    except:
        return ["Bangalore", "Delhi", "Mumbai", "New York"]

city_list = load_cities()

# Weather condition media mapping
weather_media = {
    "Clear":    {"icon": "☀️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Clouds":   {"icon": "☁️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Rain":     {"icon": "🌧️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Drizzle":  {"icon": "🌦️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Thunderstorm": {"icon": "⛈️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Snow":     {"icon": "❄️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Mist":     {"icon": "🌫️", "video": "https://youtu.be/LlgLUQ2tx10"},
    "Default":  {"icon": "🌈", "video": "https://youtu.be/LlgLUQ2tx10"}
}

# Error Handler
def show_error():
    st.error("💥 Weather server dodged our request like a ninja! Try again or check your city name.")

# Weather Fetcher
def get_weather(city, units="metric"):
    try:
        API_KEY = "4d8fb5b93d4af21d66a2948710284366"
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
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

st.write("Start typing your city name and pick from the list:")

# City Selector
city = st.selectbox("📍 Choose your city", options=city_list, index=city_list.index("Delhi") if "Delhi" in city_list else 0)

# Get Weather Button
if st.button("🔍 Get Forecast"):
    data = get_weather(city)

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
            st.markdown(f"<h2 style='color:#f39c12;'>{media['icon']} Weather in <strong>{city.title()}</strong></h2>", unsafe_allow_html=True)
            st.write(f"**Condition:** {weather_desc}")
            st.write(f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)")
            st.write(f"💧 Humidity: {humidity}%")
            st.write(f"💨 Wind Speed: {wind_speed} m/s")

        with col2:
            st.markdown("### Weather vibes 🎥")
            st.markdown(f"""
                <div style="position: relative; width: 50%; max-width: 600px; padding-top: 50%;">
                    <iframe src="{media['video'].replace('youtu.be/', 'www.youtube.com/embed/')}?autoplay=1&start=5&mute=1"
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
