import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os

# Calculate dates
today = datetime.now()
week_ago = today - timedelta(days=7)

# Format dates for API (YYYY-MM-DD)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

city_coordinates = {
    'Lviv': (49.84, 24.03),
    'Kyiv': (50.45, 30.52),
    'Lutsk': (50.75, 25.33),
    'Kharkiv': (49.99, 36.23),
    'Dnipro': (48.45, 35.05),
    'Odesa': (46.48, 30.73),
    'Simferopol': (44.95, 34.10)
}

# Input city name
city_name = input("Enter city name (Lviv, Kyiv, Lutsk, Kharkiv, Dnipro, Odesa): ")
if city_name in city_coordinates:
    latitude, longitude = city_coordinates[city_name]
else:
    print("City not found. Using default coordinates for Lviv.")
    latitude, longitude = city_coordinates['Lviv']

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

response = requests.get(url)
data = response.json()
print(data)

#-------------------------------------------------------------
# Pandas
#-------------------------------------------------------------

# Extract the daily data
daily_data = data['daily']

# Create a DataFrame
df = pd.DataFrame({
    'date': daily_data['time'],
    'max_temp': daily_data['temperature_2m_max'],
    'min_temp': daily_data['temperature_2m_min']
})

# Convert date strings to datetime
df['date'] = pd.to_datetime(df['date'])

print(df)

#--------------------------------------------------------------
# Matplotlib
#--------------------------------------------------------------

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['max_temp'], marker='o', label='Max Temp')
plt.plot(df['date'], df['min_temp'], marker='o', label='Min Temp')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title(f'{city_name} Weather - Past 7 Days')
plt.legend()

# Rotate x-axis labels for readability
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('weather_chart.png')
plt.show()

#--------------------------------------------------------------
# File Handling
#--------------------------------------------------------------

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Save to CSV
df.to_csv(f'data/{city_name.lower()}_weather.csv', index=False)
print(f"Data saved to data/{city_name.lower()}_weather.csv")