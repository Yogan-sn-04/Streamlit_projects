import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Weather Wizard 🌦️", page_icon="🌦️", layout="wide")

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

# Weather Fetcher (Forecast)
def get_weather_forecast(city, country, units="metric"):
    try:
        API_KEY = "4d8fb5b93d4af21d66a2948710284366"
        query = f"{city},{country}"
        URL = f"http://api.openweathermap.org/data/2.5/forecast?q={query}&appid={API_KEY}&units={units}"
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
    with st.spinner("Fetching weather data..."):
        forecast_data = get_weather_forecast(selected_city, selected_country)

    if forecast_data:
        df = pd.DataFrame(forecast_data['list'])
        df['dt'] = pd.to_datetime(df['dt'], unit='s')
        df['date'] = df['dt'].dt.date
        df['hour'] = df['dt'].dt.hour

        # Get one forecast per day closest to 12PM
        daily_forecast = df[df['hour'] == 12].groupby('date').first().head(5)

        st.markdown(f"### 🌤️ 5-Day Forecast for **{selected_city.title()}, {selected_country}**")

        for _, row in daily_forecast.iterrows():
            weather_main = row['weather'][0]['main']
            weather_desc = row['weather'][0]['description'].capitalize()
            temp = row['main']['temp']
            feels_like = row['main']['feels_like']
            humidity = row['main']['humidity']
            wind_speed = row['wind']['speed']
            date_str = row['dt'].strftime("%A, %d %b %Y")

            media = weather_media.get(weather_main, weather_media["Default"])

            with st.container():
                st.markdown(f"#### {media['icon']} {date_str}")
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Condition:** {weather_desc}")
                    st.write(f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)")
                    st.write(f"💧 Humidity: {humidity}%")
                    st.write(f"💨 Wind Speed: {wind_speed} m/s")
                with col2:
                    st.image(f"https://openweathermap.org/img/wn/{row['weather'][0]['icon']}@2x.png", width=80)

            st.markdown("---")

        st.caption("🌍 Powered by OpenWeatherMap & curated weather videos 🎬")

    else:
        show_error()
