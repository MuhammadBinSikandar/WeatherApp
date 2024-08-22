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

NUTECH_temperature = 33
NUTECH_humidity = 50
NUTECH_pressure = 1013
NUTECH_rain = 0
NUTECH_wind_direction = "North"
NUTECH_wind_speed = 10
NUTECH_solar_radiation = 100
NUTECH_evapotranspiration = 0
NUTECH_pollen_count = 0
NUTECH_optical_particles = 0
NUTECH_co2_level = 600
NUTECH_soil_moisture = 20

Margalla_temperature = 33
Margalla_humidity = 50
Margalla_pressure = 1013
Margalla_rain = 0
Margalla_wind_direction = "North"
Margalla_wind_speed = 10
Margalla_solar_radiation = 100
Margalla_evapotranspiration = 0
Margalla_pollen_count = 0
Margalla_optical_particles = 0
Margalla_co2_level = 600
Margalla_soil_moisture = 20


def dataScrapping(database = "NUTECH", 
                  station = "IISLAM48",
                  opticalParticleUrl = "https://www.iqair.com/pakistan/islamabad",
                  soilMoistureUrl = "https://api.thingspeak.com/channels/2597059/fields/1.json?results=2",
                  co2Url = "https://api.thingspeak.com/channels/2611683/feeds.json?results=1"):
    
    client = MongoClient("mongodb+srv://niclab747:Q2AIeeHH4As1aSFc@weatherapplication.dsm8c7f.mongodb.net/?retryWrites=true&w=majority&appName=WeatherApplication")

    
    if database == "NUTECH":
        global NUTECH_temperature, NUTECH_humidity, NUTECH_pressure, NUTECH_rain, NUTECH_wind_direction, NUTECH_wind_speed, NUTECH_solar_radiation, NUTECH_evapotranspiration, NUTECH_pollen_count, NUTECH_optical_particles, NUTECH_co2_level, NUTECH_soil_moisture
    else:
        global Margalla_temperature, Margalla_humidity, Margalla_pressure, Margalla_rain, Margalla_wind_direction, Margalla_wind_speed, Margalla_solar_radiation, Margalla_evapotranspiration, Margalla_pollen_count, Margalla_optical_particles, Margalla_co2_level, Margalla_soil_moisture
    pakistan_timezone = timezone(timedelta(hours=5))
    today_date = datetime.now(pakistan_timezone).strftime('%Y-%m-%d')
    db = client[database]
    collection = db[today_date]
    # collection = db['2024-07-15']

    weather_url = f'https://www.wunderground.com/dashboard/pws/{station}/table/{today_date}/{today_date}/daily'
    # weather_url = f'https://www.wunderground.com/dashboard/pws/IISLAM48/table/2024-07-15/2024-07-15/daily'
    weather_page = requests.get(weather_url)

    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
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
        if database == "NUTECH":
            soil_moisture = NUTECH_soil_moisture
        else:
            soil_moisture = Margalla_soil_moisture
        
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
        if database == "NUTECH":
            total_pollen = NUTECH_pollen_count
        else:
            total_pollen = Margalla_pollen_count
    if len(digits) > 1:    
        total_pollen = str(digits[0])+str(digits[1])
    else:   
        total_pollen = digits[0]
    total_pollen = int(total_pollen)
    if database == "NUTECH":
        total_pollen = total_pollen - random.randint(50, 60)
    else:
        total_pollen = total_pollen + random.randint(50, 60)

    optical_particle_response.raise_for_status()
    optical_particle_soup = BeautifulSoup(optical_particle_response.content, 'html.parser')
    optical_particle_count = optical_particle_soup.find(class_="mat-tooltip-trigger pollutant-concentration-value")
    if not optical_particle_count:
        if database == "NUTECH":
            optical_particles = NUTECH_optical_particles
        else:
            optical_particles = Margalla_optical_particles
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
                if database == "NUTECH":
                    individual_row_data["Temperature (°C)"] = NUTECH_temperature
                else:
                    individual_row_data["Temperature (°C)"] = Margalla_temperature
            else:
                individual_row_data["Temperature (°C)"] = round((float(individual_row_data['Temperature (°C)']) - 32) * 5 / 9, 1)

            individual_row_data["Humidity (%)"] = individual_row_data["Humidity"].split()[0]
            del individual_row_data["Humidity"]
            if individual_row_data["Humidity (%)"] == '--':
                if database == "NUTECH":
                    individual_row_data["Humidity (%)"] = NUTECH_humidity
                else:
                    individual_row_data["Humidity (%)"] = Margalla_humidity
            else:
                individual_row_data["Humidity (%)"] = int(individual_row_data["Humidity (%)"])

            individual_row_data["Pressure (hPa)"]= individual_row_data["Pressure"].split()[0]
            del individual_row_data["Pressure"]
            if individual_row_data["Pressure (hPa)"] == '--':
                if database == "NUTECH":
                    individual_row_data["Pressure (hPa)"] = NUTECH_pressure
                else:
                    individual_row_data["Pressure (hPa)"] = Margalla_pressure
            else:
                individual_row_data["Pressure (hPa)"] = round(float(individual_row_data["Pressure (hPa)"]) * 33.863889532610884, 1)

            individual_row_data["Rain (mm)"] = individual_row_data["Precip. Accum."].split()[0]
            del individual_row_data["Precip. Accum."]
            if individual_row_data["Rain (mm)"] == '--':
                if database == "NUTECH":
                    individual_row_data["Rain (mm)"] = NUTECH_rain
                else:
                    individual_row_data["Rain (mm)"] = Margalla_rain
            else:
                individual_row_data["Rain (mm)"] = round(float(individual_row_data["Rain (mm)"]) * 25.4, 1)

            individual_row_data["Wind Direction"] = individual_row_data["Wind"]
            del individual_row_data["Wind"]
            if individual_row_data["Wind Direction"] == '':
                if database == "NUTECH":
                    individual_row_data["Wind Direction"] = NUTECH_wind_direction
                else:
                    individual_row_data["Wind Direction"] = Margalla_wind_direction

            individual_row_data["Wind Speed (km/h)"] = individual_row_data["Speed"].split()[0]
            del individual_row_data["Speed"]
            if individual_row_data["Wind Speed (km/h)"] == '--':
                if database == "NUTECH":
                    individual_row_data["Wind Speed (km/h)"] = NUTECH_wind_speed
                else:
                    individual_row_data["Wind Speed (km/h)"] = Margalla_wind_speed
            else:
                individual_row_data["Wind Speed (km/h)"] = round(float(individual_row_data["Wind Speed (km/h)"]) * 1.60934, 1)

            individual_row_data["Solar Radiation (w/m²)"] = individual_row_data["Solar"].split()[0]
            del individual_row_data["Solar"]
            if individual_row_data["Solar Radiation (w/m²)"] == '--' or individual_row_data["Solar Radiation (w/m²)"] == 'w/m²':
                if database == "NUTECH":
                    individual_row_data["Solar Radiation (w/m²)"] = NUTECH_solar_radiation
                else:
                    individual_row_data["Solar Radiation (w/m²)"] = Margalla_solar_radiation
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

    if database == "NUTECH":
        NUTECH_temperature = individual_row_data["Temperature (°C)"]
        NUTECH_humidity = individual_row_data["Humidity (%)"]
        NUTECH_pressure = individual_row_data["Pressure (hPa)"]
        NUTECH_rain = individual_row_data["Rain (mm)"]
        NUTECH_wind_direction = individual_row_data["Wind Direction"]
        NUTECH_wind_speed = individual_row_data["Wind Speed (km/h)"]
        NUTECH_solar_radiation = individual_row_data["Solar Radiation (w/m²)"]
        NUTECH_evapotranspiration = individual_row_data["Evapotranspiration"]
        NUTECH_pollen_count = individual_row_data["Pollen Count (g/m)"]
        NUTECH_optical_particles = individual_row_data["Optical Particles (g/m)"]
        NUTECH_co2_level = individual_row_data["CO2 level (ppm)"]
        NUTECH_soil_moisture = individual_row_data["Soil Moisture (kPa)"]
    else:
        Margalla_temperature = individual_row_data["Temperature (°C)"]
        Margalla_humidity = individual_row_data["Humidity (%)"]
        Margalla_pressure = individual_row_data["Pressure (hPa)"]
        Margalla_rain = individual_row_data["Rain (mm)"]
        Margalla_wind_direction = individual_row_data["Wind Direction"]
        Margalla_wind_speed = individual_row_data["Wind Speed (km/h)"]
        Margalla_solar_radiation = individual_row_data["Solar Radiation (w/m²)"]
        Margalla_evapotranspiration = individual_row_data["Evapotranspiration"]
        Margalla_pollen_count = individual_row_data["Pollen Count (g/m)"]
        Margalla_optical_particles = individual_row_data["Optical Particles (g/m)"]
        Margalla_co2_level = individual_row_data["CO2 level (ppm)"]
        Margalla_soil_moisture = individual_row_data["Soil Moisture (kPa)"]            
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

    # Mapping the predictions according to the data for the day number
    weather_forecast = []

    for i, day in enumerate(data['daily']['time']):
        forecast = {
            'high_temp': data['daily']['temperature_2m_max'][i],
            'low_temp': data['daily']['temperature_2m_min'][i],
            'uv': data['daily']['uv_index_max'][i],
            'precipitation': data['daily']['precipitation_sum'][i],
            'wind_speed': data['daily']['wind_speed_10m_max'][i]
        }
        weather_forecast.append(forecast)

    for i, forecast in enumerate(weather_forecast):
        forecast['High_Temperature'] = int(forecast['high_temp'])
        del forecast['high_temp']
        forecast['Low_Temperature'] = int(forecast['low_temp'])
        del forecast['low_temp']
        forecast['Day_Number'] = i + 1
        predictions_collection.insert_one(forecast)



pakistan_timezone = timezone(timedelta(hours=5))
today_date = datetime.now(pakistan_timezone).strftime('%Y-%m-%d')


def start_schedule():
    schedule.every(15).minutes.do(dataScrapping, "NUTECH", "IISLAM48", 
                                  "https://www.iqair.com/pakistan/islamabad/austrian-embassy", 
                                  "https://api.thingspeak.com/channels/2597059/fields/1.json?results=2", 
                                  "https://api.thingspeak.com/channels/2598253/feeds.json?results=1")
    schedule.every(15).minutes.do(dataScrapping, "Margalla", "IISLAM50", 
                                  "https://www.iqair.com/pakistan/islamabad/house%238-maain-khayaban-e-iqbal-f-6-3", 
                                  "https://api.thingspeak.com/channels/2611688/fields/1.json?results=2", 
                                  "https://api.thingspeak.com/channels/2611683/feeds.json?results=1")
    
    schedule.every().day.at("00:00").do(predictions, "NUTECH", search="https://api.open-meteo.com/v1/forecast?latitude=33.62599&longitude=73.01109&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=Asia%2FSingapore")
    schedule.every().day.at("00:00").do(predictions, "Margalla", search="https://api.open-meteo.com/v1/forecast?latitude=33.759271&longitude=73.08361&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=Asia%2FSingapore")
    schedule.every().day.at("12:00").do(predictions, "NUTECH", search="https://api.open-meteo.com/v1/forecast?latitude=33.62599&longitude=73.01109&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=Asia%2FSingapore")
    schedule.every().day.at("12:00").do(predictions, "Margalla", search="https://api.open-meteo.com/v1/forecast?latitude=33.759271&longitude=73.08361&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=Asia%2FSingapore")
    
    dataScrapping(database="NUTECH", 
                  station = "IISLAM48", 
                  opticalParticleUrl="https://www.iqair.com/pakistan/islamabad/austrian-embassy",
                  soilMoistureUrl="https://api.thingspeak.com/channels/2597059/fields/1.json?results=2",
                  co2Url="https://api.thingspeak.com/channels/2598253/feeds.json?results=1")
    dataScrapping(database="Margalla", 
                  station = "IISLAM50", 
                  opticalParticleUrl="https://www.iqair.com/pakistan/islamabad/house%238-maain-khayaban-e-iqbal-f-6-3",
                  soilMoistureUrl="https://api.thingspeak.com/channels/2611688/fields/1.json?results=2",
                  co2Url="https://api.thingspeak.com/channels/2611683/feeds.json?results=1")
    
    predictions(database="NUTECH" ,api_url="https://api.open-meteo.com/v1/forecast?latitude=33.62599&longitude=73.01109&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=Asia%2FSingapore")
    predictions(database="Margalla" ,api_url="https://api.open-meteo.com/v1/forecast?latitude=33.759271&longitude=73.08361&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,wind_speed_10m_max&timezone=Asia%2FSingapore")

    while True:
        schedule.run_pending()
        time.sleep(1)


<<<<<<< HEAD
global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH, mapped_all_data_Margalla
=======
<<<<<<< HEAD
global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH, mapped_all_data_Margalla
=======
global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH
>>>>>>> d6eb8847b9f0289418c744ba86fad811561abc03
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
global predictions_by_day_NUTECH, predictions_by_day_Margalla, mapped_weekly_data_NUTECH, mapped_monthly_data_NUTECH
global aggregated_weekly_data_NUTECH, aggregated_weekly_data_Margalla
global aggregated_monthly_data_NUTECH, aggregated_monthly_data_Margalla
global temperature_graph_html_day, humidity_graph_html_day, pressure_graph_html_day, temperature_graph_html_week, humidity_graph_html_week 
global pressure_graph_html_week, temperature_graph_html_month, humidity_graph_html_month, pressure_graph_html_month 

def get_data_from_db():
<<<<<<< HEAD
    global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH, mapped_all_data_Margalla
=======
<<<<<<< HEAD
    global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH, mapped_all_data_Margalla
=======
    global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH
>>>>>>> d6eb8847b9f0289418c744ba86fad811561abc03
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
    global predictions_by_day_NUTECH, predictions_by_day_Margalla, mapped_weekly_data_NUTECH, mapped_monthly_data_NUTECH
    global aggregated_weekly_data_NUTECH, aggregated_weekly_data_Margalla
    global aggregated_monthly_data_NUTECH, aggregated_monthly_data_Margalla
    global temperature_graph_html_day, humidity_graph_html_day, pressure_graph_html_day, temperature_graph_html_week, humidity_graph_html_week 
    global pressure_graph_html_week, temperature_graph_html_month, humidity_graph_html_month, pressure_graph_html_month 
    client = MongoClient("mongodb+srv://niclab747:Q2AIeeHH4As1aSFc@weatherapplication.dsm8c7f.mongodb.net/?retryWrites=true&w=majority&appName=WeatherApplication")

    Today_date = datetime.now()

    pakistan_timezone = timezone(timedelta(hours=5))
    formatted_date = datetime.now(pakistan_timezone).strftime('%Y-%m-%d')

    db1 = client["NUTECH"]
    collection_NUTECH = db1[formatted_date]
    predictions_NUTECH = db1['predictions']

    db2 = client["Margalla"]
    collection_Margalla = db2[formatted_date]
    predictions_Margalla = db2['predictions']

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

    last_data_NUTECH = collection_NUTECH.find().sort('_id', -1).limit(1)[0]
    last_data_Margalla = collection_Margalla.find().sort('_id', -1).limit(1)[0]

    weekly_data_NUTECH = get_data_for_period(db1, one_week_ago, Today_date)
    weekly_data_Margalla = get_data_for_period(db2, one_week_ago, Today_date)

    monthly_data_NUTECH = get_data_for_period(db1, one_month_ago, Today_date)
    monthly_data_Margalla = get_data_for_period(db2, one_month_ago, Today_date)

    all_data_NUTECH = collection_NUTECH.find().sort('_id', 1)
    all_data_Margalla = collection_Margalla.find().sort('_id', 1)

    mapped_last_data_NUTECH = map_data1(last_data_NUTECH)
    mapped_last_data_Margalla = map_data1(last_data_Margalla)

    mapped_all_data_NUTECH = [map_data1(data) for data in all_data_NUTECH]
    mapped_all_data_Margalla = [map_data1(data) for data in all_data_Margalla]

    mapped_weekly_data_NUTECH = [map_data(data) for data in weekly_data_NUTECH]
    mapped_weekly_data_Margalla = [map_data(data) for data in weekly_data_Margalla]

    mapped_monthly_data_NUTECH = [map_data(data) for data in monthly_data_NUTECH]
    mapped_monthly_data_Margalla = [map_data(data) for data in monthly_data_Margalla]

    aggregated_weekly_data_NUTECH = aggregate_data_by_date(mapped_weekly_data_NUTECH)
    aggregated_weekly_data_Margalla = aggregate_data_by_date(mapped_weekly_data_Margalla)

    aggregated_monthly_data_NUTECH = aggregate_data_by_date(mapped_monthly_data_NUTECH)
    aggregated_monthly_data_Margalla = aggregate_data_by_date(mapped_monthly_data_Margalla)

    all_data_NUTECH = list(mapped_all_data_NUTECH)
    all_data_Margalla = list(mapped_all_data_Margalla)

    min_length = min(len(all_data_NUTECH), len(all_data_Margalla))
    all_data_NUTECH = all_data_NUTECH[:min_length]
    all_data_Margalla = all_data_Margalla[:min_length]

    combined_data = list(zip(all_data_NUTECH, all_data_Margalla))

    prediction_data_NUTECH = predictions_NUTECH.find()
    prediction_data_Margalla = predictions_Margalla.find()
    
    predictions_by_day_NUTECH = {}
    for data in prediction_data_NUTECH:
        day_number = data['Day_Number']
        temperature = data['High_Temperature']
        high_temperature = data['High_Temperature']
        low_temperature = data['Low_Temperature']
        Wind_Speed = data['wind_speed']
        precipitation = data['precipitation']
        predictions_by_day_NUTECH[day_number] = {'Temperature': temperature, 'High_Temperature': high_temperature, 'Low_Temperature': low_temperature, 'Wind_Speed': Wind_Speed, 'Precipitation': precipitation}

    predictions_by_day_Margalla = {}
    for data in prediction_data_Margalla:
        day_number = data['Day_Number']
        temperature = data['High_Temperature']
        high_temperature = data['High_Temperature']
        low_temperature = data['Low_Temperature']
        Wind_Speed = data['wind_speed']
        precipitation = data['precipitation']
        predictions_by_day_Margalla[day_number] = {'Temperature': temperature, 'High_Temperature': high_temperature, 'Low_Temperature': low_temperature, 'Wind_Speed': Wind_Speed, 'Precipitation': precipitation}

<<<<<<< HEAD


    def create_graph(x_data, y_data_NUTECH, y_data_Margalla, yaxis_title, color1="orange", color2="blue"):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, 
                                 y=y_data_NUTECH, 
                                 mode='lines', 
                                 line=dict(color=color1, width=5), 
                                 name='NUTECH'))
        fig.add_trace(go.Scatter(x=x_data, 
                                 y=y_data_Margalla, 
                                 mode='lines', 
                                 line=dict(color=color2, width=5), 
                                 name='Margalla'))
        
        fig.update_layout(
            yaxis=dict(color='white', autorange=True),
            xaxis=dict(color='white', showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0.3)',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=30, b=20),
            autosize=True,
            legend=dict(x=1, y=1.08, xanchor='right', yanchor='top'),
        )
        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text=yaxis_title)
        return to_html(fig, config={'displayModeBar': False, 'responsive': True}, full_html=True)

    # x_data_day = [item['Time'] for item in mapped_all_data_NUTECH]
    # temperature_graph_html_day = create_graph(x_data_day, [item['Temperature'] for item in mapped_all_data_NUTECH], [item['Temperature'] for item in mapped_all_data_Margalla], 'Temperature', color1 = "orange", color2 = "blue")
    # humidity_graph_html_day = create_graph(x_data_day, [item['Humidity'] for item in mapped_all_data_NUTECH], [item['Humidity'] for item in mapped_all_data_Margalla], 'Humidity', color1="green", color2="red")
    # pressure_graph_html_day = create_graph(x_data_day, [item['Pressure'] for item in mapped_all_data_NUTECH], [item['Pressure'] for item in mapped_all_data_Margalla], 'Pressure', color1="fuchsia", color2="yellow")

    # # Create weekly graphs
    # x_data_week = list(set(item['CollectionDate'] for item in mapped_weekly_data_NUTECH))
    # x_data_week.sort()
    # temperature_graph_html_week = create_graph(x_data_week, [aggregated_weekly_data_NUTECH[f'{date}_Temperature'] for date in x_data_week], [aggregated_weekly_data_Margalla[f'{date}_Temperature'] for date in x_data_week], 'Temperature', color1 = "orange", color2 = "blue")
    # humidity_graph_html_week = create_graph(x_data_week, [aggregated_weekly_data_NUTECH[f'{date}_Humidity'] for date in x_data_week], [aggregated_weekly_data_Margalla[f'{date}_Humidity'] for date in x_data_week], 'Humidity', color1="green", color2="red")
    # pressure_graph_html_week = create_graph(x_data_week, [aggregated_weekly_data_NUTECH[f'{date}_Pressure'] for date in x_data_week], [aggregated_weekly_data_Margalla[f'{date}_Pressure'] for date in x_data_week], 'Pressure', color1="fuchsia", color2="yellow")

    # # Create monthly graphs
    # x_data_month = list(set(item['CollectionDate'] for item in mapped_monthly_data_NUTECH))
    # x_data_month.sort()
    # temperature_graph_html_month = create_graph(x_data_month, [aggregated_monthly_data_NUTECH[f'{date}_Temperature'] for date in x_data_month], [aggregated_monthly_data_Margalla[f'{date}_Temperature'] for date in x_data_month], 'Temperature', color1 = "orange", color2 = "blue")
    # humidity_graph_html_month = create_graph(x_data_month, [aggregated_monthly_data_NUTECH[f'{date}_Humidity'] for date in x_data_month], [aggregated_monthly_data_Margalla[f'{date}_Humidity'] for date in x_data_month], 'Humidity', color1="green", color2="red")
    # pressure_graph_html_month = create_graph(x_data_month, [aggregated_monthly_data_NUTECH[f'{date}_Pressure'] for date in x_data_month], [aggregated_monthly_data_Margalla[f'{date}_Pressure'] for date in x_data_month], 'Pressure', color1="fuchsia", color2="yellow")

=======
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
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
<<<<<<< HEAD
    global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH, mapped_all_data_Margalla
=======
<<<<<<< HEAD
    global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH, mapped_all_data_Margalla
=======
    global mapped_last_data_NUTECH, mapped_last_data_Margalla, combined_data, mapped_all_data_NUTECH
>>>>>>> d6eb8847b9f0289418c744ba86fad811561abc03
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
    global predictions_by_day_NUTECH, predictions_by_day_Margalla, mapped_weekly_data_NUTECH, mapped_monthly_data_NUTECH
    global aggregated_weekly_data_NUTECH, aggregated_weekly_data_Margalla
    global aggregated_monthly_data_NUTECH, aggregated_monthly_data_Margalla
    global temperature_graph_html_day, humidity_graph_html_day, pressure_graph_html_day
    global temperature_graph_html_week, humidity_graph_html_week, pressure_graph_html_week
    global temperature_graph_html_month, humidity_graph_html_month, pressure_graph_html_month

    Today_date = datetime.now()
    formatted_date = Today_date.strftime("%B %d, %Y")

    # today = datetime.now().date()
    # day_names = ['Today', 'Tomorrow']
    
    # for i in range(2, 9):  
    #     future_day = today + timedelta(days=i)
    #     day_names.append(future_day.strftime('%A %d'))

    
    context = {
        'formatted_date': formatted_date,
        # 'last_data_NUTECH': mapped_last_data_NUTECH,
        # 'last_data_Margalla': mapped_last_data_Margalla,
        'combined_data': combined_data,
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
        'mapped_all_data_NUTECH': json.dumps(mapped_all_data_NUTECH),
        'mapped_all_data_Margalla': json.dumps(mapped_all_data_Margalla),
        'mapped_weekly_data_NUTECH': json.dumps(mapped_weekly_data_NUTECH),
        'aggregated_weekly_data_NUTECH': json.dumps(aggregated_weekly_data_NUTECH),
        'aggregated_weekly_data_Margalla': json.dumps(aggregated_weekly_data_Margalla),
        'mapped_monthly_data_NUTECH': json.dumps(mapped_monthly_data_NUTECH),
        'aggregated_monthly_data_NUTECH': json.dumps(aggregated_monthly_data_NUTECH),
        'aggregated_monthly_data_Margalla': json.dumps(aggregated_monthly_data_Margalla),
<<<<<<< HEAD
=======
=======
        'mapped_all_data_NUTECH' : mapped_all_data_NUTECH,
>>>>>>> d6eb8847b9f0289418c744ba86fad811561abc03
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
        # 'predictions_day_1_NUTECH': predictions_by_day_NUTECH.get(1, {}),
        # 'predictions_day_2_NUTECH': predictions_by_day_NUTECH.get(2, {}),
        # 'predictions_day_3_NUTECH': predictions_by_day_NUTECH.get(3, {}),
        # 'predictions_day_4_NUTECH': predictions_by_day_NUTECH.get(4, {}),
        # 'predictions_day_5_NUTECH': predictions_by_day_NUTECH.get(5, {}),
        # 'predictions_day_6_NUTECH': predictions_by_day_NUTECH.get(6, {}),
        # 'predictions_day_7_NUTECH': predictions_by_day_NUTECH.get(7, {}),
        # 'predictions_day_1_Margalla': predictions_by_day_Margalla.get(1, {}),
        # 'predictions_day_2_Margalla': predictions_by_day_Margalla.get(2, {}),
        # 'predictions_day_3_Margalla': predictions_by_day_Margalla.get(3, {}),
        # 'predictions_day_4_Margalla': predictions_by_day_Margalla.get(4, {}),
        # 'predictions_day_5_Margalla': predictions_by_day_Margalla.get(5, {}),
        # 'predictions_day_6_Margalla': predictions_by_day_Margalla.get(6, {}),
        # 'predictions_day_7_Margalla': predictions_by_day_Margalla.get(7, {}),
        # 'day_name_1': day_names[0],
        # 'day_name_2': day_names[1],
        # 'day_name_3': day_names[2],
        # 'day_name_4': day_names[3],
        # 'day_name_5': day_names[4],
        # 'day_name_6': day_names[5],
        # 'day_name_7': day_names[6],
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
        # 'temperature_graph_html_day': temperature_graph_html_day,
        # 'humidity_graph_html_day': humidity_graph_html_day,
        # 'pressure_graph_html_day': pressure_graph_html_day,
        # 'temperature_graph_html_week': temperature_graph_html_week,
        # 'humidity_graph_html_week': humidity_graph_html_week,
        # 'pressure_graph_html_week': pressure_graph_html_week,
        # 'temperature_graph_html_month': temperature_graph_html_month,
        # 'humidity_graph_html_month': humidity_graph_html_month,
        # 'pressure_graph_html_month': pressure_graph_html_month,
>>>>>>> d6eb8847b9f0289418c744ba86fad811561abc03
>>>>>>> e9ea83a5d4e69b794902ce86969f46298c5b08e0
    }

    return render(request, 'index.html', context)