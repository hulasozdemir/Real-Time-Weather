import requests
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


API_KEY = 'API_Key'
LOCATION = 'Vancouver'



def fetch_weather_data():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data


while True:
    weather_data = fetch_weather_data()
    producer.send('weather_topic', value=weather_data)
    print(f"Sent data to Kafka: {weather_data}")
    time.sleep(300)  # Fetch data every 5 minutes