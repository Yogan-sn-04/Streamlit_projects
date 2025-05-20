import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Weather Wizard 🌦️", page_icon="🌦️", layout="wide")

# Load City + Country List with Bangalore Localities
@st.cache_data
def load_city_country_pairs():
    try:
        df = pd.read_csv("worldcities.csv")
        df = df[['city', 'country']].dropna().drop_duplicates()
        df['label'] = df['city'] + ", " + df['country']

        # Add Bangalore localities manually
        bangalore_areas = [
            "Koramangala", "Indiranagar", "Whitefield", "BTM Layout",
            "Electronic City", "Hebbal", "Marathahalli", "HSR Layout",
            "Jayanagar", "Rajajinagar", "Malleshwaram", "Banashankari",
            "Basavanagudi", "Yelahanka", "Sarjapur", "JP Nagar"
        ]
        blr_df = pd.DataFrame({
            "city": bangalore_areas,
            "country": ["India"] * len(bangalore_areas),
        })
        blr_df["label"] = blr_df["city"] + ", India"

        df = pd.concat([df, blr_df], ignore_index=True)
        return df.sort_values('label'), bangalore_areas
    except:
        fallback = pd.DataFrame({'label': ["Delhi, India", "Mumbai, India", "New York, United States"]})
        return fallback, []

city_df, bangalore_areas = load_city_country_pairs()

# Weather media mapping
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

# Title
st.markdown("""
    <h1 style='text-align:center; color:#4B89DC; font-family: "Segoe UI", sans-serif;'>
        🧙‍♂️ Weather Wizard 🌦️
    </h1>
""", unsafe_allow_html=True)

st.write("Start typing your city and country:")

# City Selector
city_label = st.selectbox(
    "📍 Choose your location (City, Country)",
    options=city_df['label'].tolist(),
    index=city_df['label'].tolist().index("Delhi, India") if "Delhi, India" in city_df['label'].tolist() else 0
)

# Extract city and country
city_row = city_df[city_df['label'] == city_label].iloc[0]
selected_city = city_row['city']
selected_country = city_row['country']

# If locality is in Bangalore areas, use Bangalore for the API
if selected_city in bangalore_areas:
    api_city = "Bangalore"
else:
    api_city = selected_city

# Get Weather Button
if st.button("🔍 Get Forecast"):
    with st.spinner("Fetching weather data..."):
        forecast_data = get_weather_forecast(api_city, selected_country)

    if forecast_data:
        df = pd.DataFrame(forecast_data['list'])
        df['dt'] = pd.to_datetime(df['dt'], unit='s')
        df['date'] = df['dt'].dt.date
        df['hour'] = df['dt'].dt.hour

        daily_forecast = df[df['hour'] == 12].groupby('date').first()
        today = pd.Timestamp.now().date()
        today_forecast = daily_forecast.loc[today] if today in daily_forecast.index else None
        next_days_forecast = daily_forecast[daily_forecast.index > today].head(5)

        # Show Today's Weather
        if today_forecast is not None:
            st.markdown(f"### 🌞 Today's Weather in **{selected_city.title()}, {selected_country}**")
            weather_main = today_forecast['weather'][0]['main']
            weather_desc = today_forecast['weather'][0]['description'].capitalize()
            temp = today_forecast['main']['temp']
            feels_like = today_forecast['main']['feels_like']
            humidity = today_forecast['main']['humidity']
            wind_speed = today_forecast['wind']['speed']
            media = weather_media.get(weather_main, weather_media["Default"])

            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"<h2 style='color:#f39c12;'>{media['icon']} Weather Today</h2>", unsafe_allow_html=True)
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

        # Next 5 Days
        st.markdown(f"### 📆 Forecast for the Next 5 Days")
        for date, row in next_days_forecast.iterrows():
            weather_main = row['weather'][0]['main']
            weather_desc = row['weather'][0]['description'].capitalize()
            temp = row['main']['temp']
            feels_like = row['main']['feels_like']
            humidity = row['main']['humidity']
            wind_speed = row['wind']['speed']
            date_str = pd.to_datetime(date).strftime("%A, %d %B %Y")
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
