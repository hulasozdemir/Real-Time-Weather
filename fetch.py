import requests
from kafka import KafkaProducer
import json
import time


import os

# Function to read API key from a text file
def read_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

# Path to the file containing the API key
api_key_file = 'apikey.txt'

# Read the API key from the file
API_KEY = read_api_key(api_key_file)

# Example usage: Print the API key (for testing purposes, remove or comment out in production)


time.sleep(30)

producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

LOCATION = 'Vancouver'



def fetch_weather_data():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data


while True:
    weather_data = fetch_weather_data()
    producer.send('weather', value=weather_data)
    print(f"Sent data to Kafka: {weather_data}")
    time.sleep(300)  # Fetch data every 5 minutes