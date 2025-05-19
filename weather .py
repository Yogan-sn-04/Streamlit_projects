import streamlit as st
import requests
import pandas as pd
# Page config
st.set_page_config(page_title="Weather Wizard 🌦️", page_icon="🌦️", layout="wide")

# Load city data (cached for performance)
@st.cache_data
def load_cities():
    try:
        df = pd.read_csv("worldcities.csv")
        return sorted(df['city'].dropna().unique().tolist())
    except:
        return ["Bangalore", "Delhi", "Mumbai", "New York"]  # fallback

city_list = load_cities()

# Map weather conditions to emojis & YouTube videos
weather_media = {
    "Clear": {
        "icon": "☀️",
        "video": "https://www.youtube.com/embed/1fLV3LnD3JU"  # sunny day video
    },
    "Clouds": {
        "icon": "☁️",
        "video": "https://www.youtube.com/embed/07rMLX9nPYI"  # cloudy sky video
    },
    "Rain": {
        "icon": "🌧️",
        "video": "https://www.youtube.com/embed/nrU4zR7QXoc"  # raining video
    },
    "Drizzle": {
        "icon": "🌦️",
        "video": "https://www.youtube.com/embed/nrU4zR7QXoc"
    },
    "Thunderstorm": {
        "icon": "⛈️",
        "video": "https://www.youtube.com/embed/tp7WbDlpbNs"  # thunderstorm video
    },
    "Snow": {
        "icon": "❄️",
        "video": "https://www.youtube.com/embed/fBvPmY9sHgY"  # snow video
    },
    "Mist": {
        "icon": "🌫️",
        "video": "https://www.youtube.com/embed/kk5zXEfPMrE"  # misty weather video
    },
    # Default fallback
    "Default": {
        "icon": "🌈",
        "video": "https://www.youtube.com/embed/UvAAvErZZf8"  # relaxing nature video
    }
}

# Counterattack error function
def show_error():
    st.error("💥 Oops! Weather server dodged our request like a ninja. Try again or check the city name.")

# Function to fetch weather data
def get_weather(city):
    try:
        API_KEY = "4d8fb5b93d4af21d66a2948710284366"  # Replace with your API key
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(URL)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None



# Title with style
st.markdown("""
    <h1 style='text-align:center; color:#4B89DC; font-family: Comic Sans MS, cursive;'>
        🧙‍♂️ Weather Wizard 🌦️
    </h1>
""", unsafe_allow_html=True)

st.write("Start typing your city name and pick from the list:")

# City selector
city = st.selectbox("📍 Choose your city", options=city_list, index=city_list.index("Delhi") if "Delhi" in city_list else 0)

# Fetch and display weather
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

        # Layout with columns
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"<h2 style='color:#f39c12;'>{media['icon']} Weather in <strong>{city.title()}</strong></h2>", unsafe_allow_html=True)
            st.write(f"**Condition:** {weather_desc}")
            st.write(f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)")
            st.write(f"💧 Humidity: {humidity}%")
            st.write(f"💨 Wind Speed: {wind_speed} m/s")

        with col2:
            # Embed YouTube video for current weather
            st.markdown("### Weather vibes 🎥")
            st.video(media['video'], start_time=5)  # start time to skip intro

        st.markdown("---")
        st.caption("🌍 Powered by OpenWeatherMap & curated weather videos 🎬")

    else:
        show_error()
