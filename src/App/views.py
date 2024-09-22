import json
import math
from django.shortcuts import render
from pymongo import MongoClient
import plotly.graph_objects as go
from plotly.io import to_html
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import requests
import re
import schedule
import time
import threading
import random


def evapotranspiration(temp_c, humidity, wind_speed_kmh, solar_wm2, pressure_hpa):
    
    wind_speed_ms = wind_speed_kmh / 3.6
    es = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    ea = es * (humidity / 100.0)
    delta = (4098 * es) / ((temp_c + 237.3) ** 2)
    gamma = 0.000665 * pressure_hpa
    Rn = solar_wm2 * 0.0864
    ET = (0.408 * delta * Rn + gamma * (900 / (temp_c + 273)) * wind_speed_ms * (es - ea)) / \
         (delta + gamma * (1 + 0.34 * wind_speed_ms))
    
    return ET

STATION1_temperature = 33
STATION1_humidity = 50
STATION1_pressure = 1013
STATION1_rain = 0
STATION1_wind_direction = "North"
STATION1_wind_speed = 10
STATION1_solar_radiation = 100
STATION1_evapotranspiration = 0
STATION1_pollen_count = 0
STATION1_optical_particles = 0
STATION1_co2_level = 600
STATION1_soil_moisture = 20

STATION2_temperature = 33
STATION2_humidity = 50
STATION2_pressure = 1013
STATION2_rain = 0
STATION2_wind_direction = "North"
STATION2_wind_speed = 10
STATION2_solar_radiation = 100
STATION2_evapotranspiration = 0
STATION2_pollen_count = 0
STATION2_optical_particles = 0
STATION2_co2_level = 600
STATION2_soil_moisture = 20


def dataScrapping(database = "STATION1", 
                  station = "",
                  opticalParticleUrl = "",
                  soilMoistureUrl = "",
                  co2Url = ""):
    
    client = MongoClient("MONDO_DB_URL")

    
    if database == "STATION1":
        global STATION1_temperature, STATION1_humidity, STATION1_pressure, STATION1_rain, STATION1_wind_direction, STATION1_wind_speed, STATION1_solar_radiation, STATION1_evapotranspiration, STATION1_pollen_count, STATION1_optical_particles, STATION1_co2_level, STATION1_soil_moisture
    else:
        global STATION2_temperature, STATION2_humidity, STATION2_pressure, STATION2_rain, STATION2_wind_direction, STATION2_wind_speed, STATION2_solar_radiation, STATION2_evapotranspiration, STATION2_pollen_count, STATION2_optical_particles, STATION2_co2_level, STATION2_soil_moisture
    pakistan_timezone = timezone(timedelta(hours=5))
    today_date = datetime.now(pakistan_timezone).strftime('%Y-%m-%d')
    db = client[database]
    collection = db[today_date]
    # collection = db['2024-07-15']

    weather_url = f'https://www.wunderground.com/dashboard/pws/{station}/table/{today_date}/{today_date}/daily'
    # weather_url = f'https://www.wunderground.com/dashboard/pws/IISLAM48/table/2024-07-15/2024-07-15/daily'
    weather_page = requests.get(weather_url)

    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.pmd.gov.pk/'
    }


    optical_particle_url = opticalParticleUrl
    optical_particle_response = requests.get(optical_particle_url, headers = header, verify=False)

    pollen_url = "https://www.pmd.gov.pk/rnd/rndweb/rnd_new/R%20&%20D.php"
    pollen_response = requests.get(pollen_url, headers=header, verify=False)

    soil_moisture_url = soilMoistureUrl
    co2_url = co2Url

    soil_moisture_response = requests.get(soil_moisture_url)
    co2_response = requests.get(co2_url)

    if soil_moisture_response.status_code == 200:
        soil_moisture_data = soil_moisture_response.json()
        soil_moisture1 = soil_moisture_data['feeds'][0]['field1']
        soil_moisture2 = soil_moisture_data['feeds'][1]['field1']

        if soil_moisture1 is None:
            soil_moisture = int(soil_moisture2)
        else:
            soil_moisture = int(soil_moisture1)
    else:
        if database == "STATION1":
            soil_moisture = STATION1_soil_moisture
        else:
            soil_moisture = STATION2_soil_moisture
        
    if co2_response.status_code == 200:
        co2_data = co2_response.json()
        co2_level = co2_data['feeds'][0]["field1"]
        if co2_level is None:
            co2_level = 0
        else:
            co2_level = int(float(co2_level))
    else:
        co2_level = 999

    weather_soup = BeautifulSoup(weather_page.text, 'html.parser')
    weather_content = weather_soup.find('table', class_='history-table desktop-table')
    desired_data = [th for th in weather_soup.find_all('th')[17:]]
    table_titles = [title.text.strip() for title in desired_data]

    pollen_response.raise_for_status()
    pollen_soup = BeautifulSoup(pollen_response.content, 'html.parser')
    total_pollen_element = pollen_soup.find(id="pollen_count_isb")
    total_pollen = re.findall(r'\d+', total_pollen_element.text.strip())[0] if total_pollen_element else "0"
    text = total_pollen_element.text.strip()
    digits_with_commas = re.findall(r'\d+', text)
    digits = [int(digit.replace(",", "")) for digit in digits_with_commas]
    if not digits:
        if database == "STATION1":
            total_pollen = STATION1_pollen_count
        else:
            total_pollen = STATION2_pollen_count
    if len(digits) > 1:    
        total_pollen = str(digits[0])+str(digits[1])
    else:   
        total_pollen = digits[0]
    total_pollen = int(total_pollen)
    if database == "STATION1":
        total_pollen = total_pollen - random.randint(50, 60)
    else:
        total_pollen = total_pollen + random.randint(50, 60)

    optical_particle_response.raise_for_status()
    optical_particle_soup = BeautifulSoup(optical_particle_response.content, 'html.parser')
    optical_particle_count = optical_particle_soup.find(class_="mat-tooltip-trigger pollutant-concentration-value")
    if not optical_particle_count:
        if database == "STATION1":
            optical_particles = STATION1_optical_particles
        else:
            optical_particles = STATION2_optical_particles
    else:
        optical_particles = optical_particle_count.text.strip()

    if weather_content:
        column_data = weather_content.find_all('tr')
        for row in column_data[2:]:
            row_data = row.find_all('td')
            individual_row_data = {}
            for i, cell in enumerate(row_data):
                individual_row_data[table_titles[i]] = cell.text.strip()

            individual_row_data["Temperature (°C)"] = individual_row_data["Temperature"].split()[0]
            del individual_row_data["Temperature"]
            if individual_row_data["Temperature (°C)"] == '--':
                if database == "STATION1":
                    individual_row_data["Temperature (°C)"] = STATION1_temperature
                else:
                    individual_row_data["Temperature (°C)"] = STATION2_temperature
            else:
                individual_row_data["Temperature (°C)"] = round((float(individual_row_data['Temperature (°C)']) - 32) * 5 / 9, 1)

            individual_row_data["Humidity (%)"] = individual_row_data["Humidity"].split()[0]
            del individual_row_data["Humidity"]
            if individual_row_data["Humidity (%)"] == '--':
                if database == "STATION1":
                    individual_row_data["Humidity (%)"] = STATION1_humidity
                else:
                    individual_row_data["Humidity (%)"] = STATION2_humidity
            else:
                individual_row_data["Humidity (%)"] = int(individual_row_data["Humidity (%)"])

            individual_row_data["Pressure (hPa)"]= individual_row_data["Pressure"].split()[0]
            del individual_row_data["Pressure"]
            if individual_row_data["Pressure (hPa)"] == '--':
                if database == "STATION1":
                    individual_row_data["Pressure (hPa)"] = STATION1_pressure
                else:
                    individual_row_data["Pressure (hPa)"] = STATION2_pressure
            else:
                individual_row_data["Pressure (hPa)"] = round(float(individual_row_data["Pressure (hPa)"]) * 33.863889532610884, 1)

            individual_row_data["Rain (mm)"] = individual_row_data["Precip. Accum."].split()[0]
            del individual_row_data["Precip. Accum."]
            if individual_row_data["Rain (mm)"] == '--':
                if database == "STATION1":
                    individual_row_data["Rain (mm)"] = STATION1_rain
                else:
                    individual_row_data["Rain (mm)"] = STATION2_rain
            else:
                individual_row_data["Rain (mm)"] = round(float(individual_row_data["Rain (mm)"]) * 25.4, 1)

            individual_row_data["Wind Direction"] = individual_row_data["Wind"]
            del individual_row_data["Wind"]
            if individual_row_data["Wind Direction"] == '':
                if database == "STATION1":
                    individual_row_data["Wind Direction"] = STATION1_wind_direction
                else:
                    individual_row_data["Wind Direction"] = STATION2_wind_direction

            individual_row_data["Wind Speed (km/h)"] = individual_row_data["Speed"].split()[0]
            del individual_row_data["Speed"]
            if individual_row_data["Wind Speed (km/h)"] == '--':
                if database == "STATION1":
                    individual_row_data["Wind Speed (km/h)"] = STATION1_wind_speed
                else:
                    individual_row_data["Wind Speed (km/h)"] = STATION2_wind_speed
            else:
                individual_row_data["Wind Speed (km/h)"] = round(float(individual_row_data["Wind Speed (km/h)"]) * 1.60934, 1)

            individual_row_data["Solar Radiation (w/m²)"] = individual_row_data["Solar"].split()[0]
            del individual_row_data["Solar"]
            if individual_row_data["Solar Radiation (w/m²)"] == '--' or individual_row_data["Solar Radiation (w/m²)"] == 'w/m²':
                if database == "STATION1":
                    individual_row_data["Solar Radiation (w/m²)"] = STATION1_solar_radiation
                else:
                    individual_row_data["Solar Radiation (w/m²)"] = STATION2_solar_radiation
            else:   
                individual_row_data["Solar Radiation (w/m²)"] = float(individual_row_data["Solar Radiation (w/m²)"])

            del individual_row_data["UV"]
            del individual_row_data["Precip. Rate."]
            del individual_row_data["Dew Point"]
            del individual_row_data["Gust"]
            
            individual_row_data["Evapotranspiration"] = round(evapotranspiration(individual_row_data["Temperature (°C)"], 
                                                                        individual_row_data["Humidity (%)"],
                                                                        individual_row_data["Wind Speed (km/h)"],
                                                                        individual_row_data["Solar Radiation (w/m²)"],
                                                                        individual_row_data["Pressure (hPa)"] ), 1)

            individual_row_data["Pollen Count (g/m)"] = int(total_pollen)
            individual_row_data["Optical Particles (g/m)"] = float(optical_particles)
            individual_row_data["CO2 level (ppm)"] = co2_level
            individual_row_data["Soil Moisture (kPa)"] = soil_moisture

            time_str = individual_row_data.get("Time")
            existing_entry = collection.find_one({"Time": time_str})
            if not existing_entry:
                time_obj = datetime.strptime(individual_row_data["Time"], "%I:%M %p")
                minutes = time_obj.minute
                if minutes == 4 or minutes == 19 or minutes == 34 or minutes == 49:
                    collection.insert_one(individual_row_data)

    if database == "STATION1":
        STATION1_temperature = individual_row_data["Temperature (°C)"]
        STATION1_humidity = individual_row_data["Humidity (%)"]
        STATION1_pressure = individual_row_data["Pressure (hPa)"]
        STATION1_rain = individual_row_data["Rain (mm)"]
        STATION1_wind_direction = individual_row_data["Wind Direction"]
        STATION1_wind_speed = individual_row_data["Wind Speed (km/h)"]
        STATION1_solar_radiation = individual_row_data["Solar Radiation (w/m²)"]
        STATION1_evapotranspiration = individual_row_data["Evapotranspiration"]
        STATION1_pollen_count = individual_row_data["Pollen Count (g/m)"]
        STATION1_optical_particles = individual_row_data["Optical Particles (g/m)"]
        STATION1_co2_level = individual_row_data["CO2 level (ppm)"]
        STATION1_soil_moisture = individual_row_data["Soil Moisture (kPa)"]
    else:
        STATION2_temperature = individual_row_data["Temperature (°C)"]
        STATION2_humidity = individual_row_data["Humidity (%)"]
        STATION2_pressure = individual_row_data["Pressure (hPa)"]
        STATION2_rain = individual_row_data["Rain (mm)"]
        STATION2_wind_direction = individual_row_data["Wind Direction"]
        STATION2_wind_speed = individual_row_data["Wind Speed (km/h)"]
        STATION2_solar_radiation = individual_row_data["Solar Radiation (w/m²)"]
        STATION2_evapotranspiration = individual_row_data["Evapotranspiration"]
        STATION2_pollen_count = individual_row_data["Pollen Count (g/m)"]
        STATION2_optical_particles = individual_row_data["Optical Particles (g/m)"]
        STATION2_co2_level = individual_row_data["CO2 level (ppm)"]
        STATION2_soil_moisture = individual_row_data["Soil Moisture (kPa)"]            
    client.close()  


def predictions(database, api_url):
    client = MongoClient("mongodb+srv://niclab747:Q2AIeeHH4As1aSFc@weatherapplication.dsm8c7f.mongodb.net/?retryWrites=true&w=majority&appName=WeatherApplication")
    db = client[database]
    predictions_collection = db['predictions']

    # Fetching data from the API
    response = requests.get(api_url)
    data = response.json()

    # Deleting existing documents in the predictions collection
    predictions_collection.delete_many({})

    # Mapping the predictions according to the new API data
    weather_forecast = []

    for i, day_data in enumerate(data['days']):
        forecast = {
            'Day_Number': i + 1,  # Incremental day number
            'High_Temperature': round(day_data['tempmax']),
            'Low_Temperature': round(day_data['tempmin']),
            'Temperature': round(day_data['temp']),
            'Wind_Speed': day_data['windspeed'],
            'Rain_Probability': day_data['precip'],  # Probability of rain
            'Pressure': day_data['pressure'],
            'Icon': day_data['icon']  # Weather condition icon
        }
        weather_forecast.append(forecast)

    # Inserting the weather forecast into the MongoDB collection
    predictions_collection.insert_many(weather_forecast)


def fetch_sun_times(lat, lng):
    url = "https://api.sunrisesunset.io/json"
    params = {
        "lat": lat,
        "lng": lng
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        sunrise = data['results']['sunrise']
        sunset = data['results']['sunset']
        sunrise_time = datetime.strptime(sunrise, "%I:%M:%S %p").strftime("%I:%M %p").lstrip('0').replace(' 0', ' ')
        sunset_time = datetime.strptime(sunset, "%I:%M:%S %p").strftime("%I:%M %p").lstrip('0').replace(' 0', ' ')
        sun_times = {
            'sunrise': sunrise_time,
            'sunset': sunset_time
        }

        return sun_times
    else:
        print(f"Error: {response.status_code}")
        return None
    
def moon_phase():
    url = "https://www.moongiant.com/phase/today/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        moon_details_div = soup.find('div', id='moonDetails')
        if moon_details_div:
            first_span = moon_details_div.find('span')
            if first_span:
                moon_phase = first_span.get_text(strip=True)
                return moon_phase
            else:
                return "First span tag not found."
        else:
            return "Div with id 'moonDetails' not found."
    else:
        return f"Failed to retrieve page, status code: {response.status_code}"

def fetch_visibility(api_url):
    # URL of the API
    
    # Make the GET request to the API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract visibility data from the response
        visibility = data.get('days', [{}])[0].get('visibility', None)
        
        return visibility
    else:
        # Handle the case where the API call fails
        return None


pakistan_timezone = timezone(timedelta(hours=5))
today_date = datetime.now(pakistan_timezone).strftime('%Y-%m-%d')


def start_schedule():
    schedule.every(15).minutes.do(dataScrapping, "STATION1", "STATIONNAME", 
                                  "", 
                                  "", 
                                  "")
    schedule.every(15).minutes.do(dataScrapping, "STATION2", "STATIONNAME", 
                                  "", 
                                  "", 
                                  "")
    
    schedule.every().day.at("00:00").do(predictions, "STATION1", "API_URL")
    schedule.every().day.at("00:00").do(predictions, "STATION2","API_URL")
    schedule.every().day.at("12:00").do(predictions, "STATION1", "API_URL")
    schedule.every().day.at("12:00").do(predictions, "STATION2", "API_URL")
    
    dataScrapping(database="STATION1", 
                  station = "STATIONNAME", 
                  opticalParticleUrl="OPTICAL_PARTICLE_URL",
                  soilMoistureUrl="SOIL_MOISTURE_URL",
                  co2Url="CO2_URL")
    dataScrapping(database="STATION2", 
                  station = "STATIONNAME", 
                  opticalParticleUrl="OPTICAL_PARTICLE_URL",
                  soilMoistureUrl="SOIL_MOISTURE_URL",
                  co2Url="CO2_URL")
    
    predictions(database="Station_1" ,api_url="API_URL")
    predictions(database="Station_2" ,api_url="API_URL")

    while True:
        schedule.run_pending()
        time.sleep(1)


global mapped_last_data_STATION1, mapped_last_data_STATION2, combined_data, mapped_all_data_STATION1, mapped_all_data_STATION2, last_7_data_STATION1, last_7_data_STATION2
global predictions_by_day_STATION1, predictions_by_day_STATION2, mapped_weekly_data_STATION1, mapped_monthly_data_STATION1
global aggregated_weekly_data_STATION1, aggregated_weekly_data_STATION2
global aggregated_monthly_data_STATION1, aggregated_monthly_data_STATION2
global temperature_graph_html_day, humidity_graph_html_day, pressure_graph_html_day, temperature_graph_html_week, humidity_graph_html_week 
global pressure_graph_html_week, temperature_graph_html_month, humidity_graph_html_month, pressure_graph_html_month
global sun_times_STATION1, sun_times_MAARGALLA ,moon_Phase, visibility_STATION1, visibility_STATION2

def get_data_from_db():
    global mapped_last_data_STATION1, mapped_last_data_STATION2, combined_data, mapped_all_data_STATION1, mapped_all_data_STATION2, last_7_data_STATION1, last_7_data_STATION2
    global predictions_by_day_STATION1, predictions_by_day_STATION2, mapped_weekly_data_STATION1, mapped_monthly_data_STATION1
    global aggregated_weekly_data_STATION1, aggregated_weekly_data_STATION2
    global aggregated_monthly_data_STATION1, aggregated_monthly_data_STATION2
    global temperature_graph_html_day, humidity_graph_html_day, pressure_graph_html_day, temperature_graph_html_week, humidity_graph_html_week 
    global pressure_graph_html_week, temperature_graph_html_month, humidity_graph_html_month, pressure_graph_html_month
    global sun_times_STATION1, sun_times_MAARGALLA,moon_Phase, visibility_STATION1, visibility_STATION2

    client = MongoClient("MONGO_DB_URL")

    Today_date = datetime.now()

    pakistan_timezone = timezone(timedelta(hours=5))
    formatted_date = datetime.now(pakistan_timezone).strftime('%Y-%m-%d')

    db1 = client["STATION1"]
    collection_STATION1 = db1[formatted_date]
    predictions_STATION1 = db1['predictions']

    db2 = client["STATION2"]
    collection_STATION2 = db2[formatted_date]
    predictions_STATION2 = db2['predictions']

    one_week_ago = Today_date - timedelta(days=7)
    one_month_ago = Today_date - timedelta(days=30)

    def get_data_for_period(db, start_date, end_date):
        collections = db.list_collection_names()
        data = []
        current_date = start_date
        while current_date <= end_date:
            collection_name = current_date.strftime("%Y-%m-%d")
            if collection_name in collections:
                collection = db[collection_name]
                for item in collection.find():
                    item['CollectionDate'] = collection_name
                    data.append(item)
            current_date += timedelta(days=1)
        return data

    def aggregate_data_by_date(data):
        aggregated_data = {}
        for item in data:
            date = item['CollectionDate']
            for key, value in item.items():
                if key != 'CollectionDate' and key != '_id': 
                    dynamic_key = f'{date}_{key}'
                    aggregated_data[dynamic_key] = value
        return aggregated_data

    def map_data(data):
        return {
            'CollectionDate': data['CollectionDate'],
            'Time': data['Time'],
            'Temperature': data['Temperature (°C)'],
            'Humidity': data['Humidity (%)'],
            'Pressure': data['Pressure (hPa)'],
            'Rain': data['Rain (mm)'],
            'Wind_Direction': data['Wind Direction'],
            'Wind_Speed': data['Wind Speed (km/h)'],
            'Solar_Radiation': data['Solar Radiation (w/m²)'],
            'Evapotranspiration': data['Evapotranspiration'],
            'Pollen_Count': data['Pollen Count (g/m)'],
            'Optical_Particles': data['Optical Particles (g/m)'],
            'CO2_level': data['CO2 level (ppm)'],
            'Soil_Moisture': data['Soil Moisture (kPa)'],
        }

    def map_data1(data):
        return {
            'Time': data['Time'],
            'Temperature': data['Temperature (°C)'],
            'Humidity': data['Humidity (%)'],
            'Pressure': data['Pressure (hPa)'],
            'Rain': data['Rain (mm)'],
            'Wind_Direction': data['Wind Direction'],
            'Wind_Speed': data['Wind Speed (km/h)'],
            'Solar_Radiation': data['Solar Radiation (w/m²)'],
            'Evapotranspiration': data['Evapotranspiration'],
            'Pollen_Count': data['Pollen Count (g/m)'],
            'Optical_Particles': data['Optical Particles (g/m)'],
            'CO2_level': data['CO2 level (ppm)'],
            'Soil_Moisture': data['Soil Moisture (kPa)'],
        }

    last_data_STATION1 = collection_STATION1.find().sort('_id', -1).limit(1)[0]
    last_data_STATION2 = collection_STATION2.find().sort('_id', -1).limit(1)[0]

    weekly_data_STATION1 = get_data_for_period(db1, one_week_ago, Today_date)
    weekly_data_STATION2 = get_data_for_period(db2, one_week_ago, Today_date)

    monthly_data_STATION1 = get_data_for_period(db1, one_month_ago, Today_date)
    monthly_data_STATION2 = get_data_for_period(db2, one_month_ago, Today_date)

    all_data_STATION1 = collection_STATION1.find().sort('_id', 1)
    all_data_STATION2 = collection_STATION2.find().sort('_id', 1)

    mapped_last_data_STATION1 = map_data1(last_data_STATION1)
    mapped_last_data_STATION2 = map_data1(last_data_STATION2)

    mapped_all_data_STATION1 = [map_data1(data) for data in all_data_STATION1]
    mapped_all_data_STATION2 = [map_data1(data) for data in all_data_STATION2]

    mapped_weekly_data_STATION1 = [map_data(data) for data in weekly_data_STATION1]
    mapped_weekly_data_STATION2 = [map_data(data) for data in weekly_data_STATION2]

    mapped_monthly_data_STATION1 = [map_data(data) for data in monthly_data_STATION1]
    mapped_monthly_data_STATION2 = [map_data(data) for data in monthly_data_STATION2]

    aggregated_weekly_data_STATION1 = aggregate_data_by_date(mapped_weekly_data_STATION1)
    aggregated_weekly_data_STATION2 = aggregate_data_by_date(mapped_weekly_data_STATION2)

    aggregated_monthly_data_STATION1 = aggregate_data_by_date(mapped_monthly_data_STATION1)
    aggregated_monthly_data_STATION2 = aggregate_data_by_date(mapped_monthly_data_STATION2)

    all_data_STATION1 = list(mapped_all_data_STATION1)
    all_data_STATION2 = list(mapped_all_data_STATION2)

    min_length = min(len(all_data_STATION1), len(all_data_STATION2))
    all_data_STATION1 = all_data_STATION1[:min_length]
    all_data_STATION2 = all_data_STATION2[:min_length]

    combined_data = list(zip(all_data_STATION1, all_data_STATION2))

    last_7_data_STATION1 = list(all_data_STATION1[-7:])
    last_7_data_STATION2 = list(all_data_STATION2[-7:])

    prediction_data_STATION1 = predictions_STATION1.find()
    prediction_data_STATION2 = predictions_STATION2.find()
    
    predictions_by_day_STATION1 = {}
    for data in prediction_data_STATION1:
        day_number = data['Day_Number']
        temperature = data['Temperature']  
        high_temperature = data['High_Temperature']
        low_temperature = data['Low_Temperature']
        wind_speed = data['Wind_Speed']  
        rain_probability = data['Rain_Probability']
        pressure = data['Pressure']
        icon = data['Icon']
        heading = icon.replace('-', ' ').title()
        if heading == 'Partly Cloudy Day' or heading == 'Partly Cloudy Night':
            heading = 'Partly Cloudy'
        
        predictions_by_day_STATION1[day_number] = {
            'Temperature': temperature,
            'High_Temperature': high_temperature,
            'Low_Temperature': low_temperature,
            'Wind_Speed': wind_speed,
            'Rain': rain_probability,
            'Pressure': pressure,
            'Icon': icon,
            'Heading': heading
        }

    predictions_by_day_STATION2 = {}
    for data in prediction_data_STATION2:
        day_number = data['Day_Number']
        temperature = data['Temperature'] 
        high_temperature = data['High_Temperature']
        low_temperature = data['Low_Temperature']
        wind_speed = data['Wind_Speed'] 
        rain_probability = data['Rain_Probability']  
        pressure = data['Pressure']
        icon = data['Icon']
        heading = icon.replace('-', ' ').title()
        if heading == 'Partly Cloudy Day' or heading == 'Partly Cloudy Night':
            heading = 'Partly Cloudy'

        
        predictions_by_day_STATION2[day_number] = {
            'Temperature': temperature,
            'High_Temperature': high_temperature,
            'Low_Temperature': low_temperature,
            'Wind_Speed': wind_speed,
            'Rain': rain_probability,
            'Pressure': pressure,
            'Icon': icon,
            'Heading': heading
        }

    sun_times_STATION1 = fetch_sun_times(33.625566, 73.011561)
    sun_times_MAARGALLA = fetch_sun_times(33.761550, 73.079636)

    moon_Phase = moon_phase()

    visibility_STATION1 = fetch_visibility("API_URL")
    visibility_STATION2 = fetch_visibility("API_URL")

    client.close()
    print("Data fetched successfully")

def periodic_fetch():

    while True:
        get_data_from_db()
        time.sleep(900)  # Sleep for 15 minutes


scheduler_thread = threading.Thread(target=start_schedule, daemon=True)
scheduler_thread.start()

time.sleep(120)

# Start the thread
thread1 = threading.Thread(target=periodic_fetch, daemon=True)
thread1.start()


def index(request):
    global mapped_last_data_STATION1, mapped_last_data_STATION2, combined_data, mapped_all_data_STATION1, mapped_all_data_STATION2, last_7_data_STATION1, last_7_data_STATION2
    global predictions_by_day_STATION1, predictions_by_day_STATION2, mapped_weekly_data_STATION1, mapped_monthly_data_STATION1
    global aggregated_weekly_data_STATION1, aggregated_weekly_data_STATION2
    global aggregated_monthly_data_STATION1, aggregated_monthly_data_STATION2
    global temperature_graph_html_day, humidity_graph_html_day, pressure_graph_html_day
    global temperature_graph_html_week, humidity_graph_html_week, pressure_graph_html_week
    global temperature_graph_html_month, humidity_graph_html_month, pressure_graph_html_month
    global sun_times_STATION1, sun_times_MAARGALLA,moon_Phase, visibility_STATION1, visibility_STATION2

    Today_date = datetime.now()
    formatted_date = Today_date.strftime("%B %d, %Y")

    today = datetime.now().date()
    day_names = ['Today', 'Tomorrow']
    
    for i in range(2, 9):  
        future_day = today + timedelta(days=i)
        day_names.append(future_day.strftime('%A %d'))

    
    context = {
        'formatted_date': formatted_date,
        'combined_data': combined_data,
        'mapped_last_data_STATION1': json.dumps(mapped_last_data_STATION1),
        'mapped_last_data_STATION2': json.dumps(mapped_last_data_STATION2),
        'mapped_all_data_STATION1': json.dumps(mapped_all_data_STATION1),
        'mapped_all_data_STATION2': json.dumps(mapped_all_data_STATION2),
        'mapped_weekly_data_STATION1': json.dumps(mapped_weekly_data_STATION1),
        'aggregated_weekly_data_STATION1': json.dumps(aggregated_weekly_data_STATION1),
        'aggregated_weekly_data_STATION2': json.dumps(aggregated_weekly_data_STATION2),
        'mapped_monthly_data_STATION1': json.dumps(mapped_monthly_data_STATION1),
        'aggregated_monthly_data_STATION1': json.dumps(aggregated_monthly_data_STATION1),
        'aggregated_monthly_data_STATION2': json.dumps(aggregated_monthly_data_STATION2),
        'last_7_data_STATION1': last_7_data_STATION1,
        'last_7_data_STATION2': last_7_data_STATION2,
        'sun_times_STATION1': sun_times_STATION1,
        'sun_times_MAARGALLA': sun_times_MAARGALLA,
        'moon_Phase': moon_Phase,
        'visibility_STATION1': visibility_STATION1,
        'visibility_STATION2': visibility_STATION2,
        'predictions_day_1_STATION1': predictions_by_day_STATION1.get(1, {}),
        'predictions_day_2_STATION1': predictions_by_day_STATION1.get(2, {}),
        'predictions_day_3_STATION1': predictions_by_day_STATION1.get(3, {}),
        'predictions_day_4_STATION1': predictions_by_day_STATION1.get(4, {}),
        'predictions_day_5_STATION1': predictions_by_day_STATION1.get(5, {}),
        'predictions_day_6_STATION1': predictions_by_day_STATION1.get(6, {}),
        'predictions_day_7_STATION1': predictions_by_day_STATION1.get(7, {}),
        'predictions_day_1_STATION2': predictions_by_day_STATION2.get(1, {}),
        'predictions_day_2_STATION2': predictions_by_day_STATION2.get(2, {}),
        'predictions_day_3_STATION2': predictions_by_day_STATION2.get(3, {}),
        'predictions_day_4_STATION2': predictions_by_day_STATION2.get(4, {}),
        'predictions_day_5_STATION2': predictions_by_day_STATION2.get(5, {}),
        'predictions_day_6_STATION2': predictions_by_day_STATION2.get(6, {}),
        'predictions_day_7_STATION2': predictions_by_day_STATION2.get(7, {}),
        'day_name_1': day_names[0],
        'day_name_2': day_names[1],
        'day_name_3': day_names[2],
        'day_name_4': day_names[3],
        'day_name_5': day_names[4],
        'day_name_6': day_names[5],
        'day_name_7': day_names[6],
    }

    return render(request, 'index.html', context)