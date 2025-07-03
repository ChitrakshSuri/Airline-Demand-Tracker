import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('AVAIATION_STACK_API_KEY')
API_URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=20"

def fetch_and_save_flight_data():
    response = requests.get(API_URL)
    data = response.json().get('data', [])

    flights = []
    for flight in data:
        airline = flight['airline']['name']
        departure = flight['departure']['airport']
        arrival = flight['arrival']['airport']
        status = flight['flight_status']
        time = flight['departure']['scheduled']
        timestamp = datetime.now().date()

        flights.append({
            'airline_name': airline,
            'from': departure,
            'to': arrival,
            'flight_status': status,
            'scheduled_time': time,
            'timestamp': timestamp
        })

    df = pd.DataFrame(flights)
    df.to_csv('api_flight_data.csv', index=False)
    print("✅ Saved to api_flight_data.csv")

if __name__ == '__main__':
    fetch_and_save_flight_data()
