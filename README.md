# Weather Data Pipeline

## Overview

This project is a data pipeline that fetches weather data from an API, processes it using Apache Spark, and stores it in Elasticsearch for visualization in Kibana.

## Setup

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
4. Create and add your API key to `apikey.txt`.

## Running the Pipeline
1. Start Apache Zookeeper: `bin/zookeeper-server-start.sh config/zookeeper.properties`
2. Start Kafka Server: `bin/kafka-server-start.sh config/server.properties`
3. Start Elasticsearch services and Kibana
4. Run the weather data fetch script: `python fetch.py`
5. Run the Spark job to process: `spark-submit --packages org.apache.spark.12:3.4.3,org.elasticsearch.12:8.14.0 scripts/weather_data_pipeline.py`

## Visualization

1. Open Kibana and create an index pattern for the `weather_index`.
2. Explore and visualize the weather data.
