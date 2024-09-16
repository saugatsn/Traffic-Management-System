import json
import random
from datetime import datetime, timedelta

def generate_traffic_data(start_time, num_days, interval_minutes):
    data = {}
    end_time = start_time + timedelta(days=num_days)
    current_time = start_time
    
    while current_time < end_time:
        current_hour = current_time.hour
        if (8 <= current_hour <= 11) or (16 <= current_hour <= 19):
            # Peak hours: reduced speed and increased volume
            road_A_data = {
                "road_id": "RA001",
                "vehicle_count": random.randint(200, 400),
                "avg_speed": random.randint(10, 40),
                "green_time": round(random.uniform(10, 20), 2),
                "red_time": round(random.uniform(15, 25), 2),
                "amber_time": 3
            }
            road_B_data = {
                "road_id": "RB001",
                "vehicle_count": random.randint(200, 400),
                "avg_speed": random.randint(10, 40),
                "green_time": round(random.uniform(10, 20), 2),
                "red_time": round(random.uniform(15, 25), 2),
                "amber_time": 3
            }
        else:
            # Non-peak hours: higher speed and lower volume
            road_A_data = {
                "road_id": "RA001",
                "vehicle_count": random.randint(50, 200),
                "avg_speed": random.randint(40, 80),
                "green_time": round(random.uniform(10, 20), 2),
                "red_time": round(random.uniform(15, 25), 2),
                "amber_time": 3
            }
            road_B_data = {
                "road_id": "RB001",
                "vehicle_count": random.randint(50, 200),
                "avg_speed": random.randint(40, 80),
                "green_time": round(random.uniform(10, 20), 2),
                "red_time": round(random.uniform(15, 25), 2),
                "amber_time": 3
            }
        
        entry = {
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "intersection_id": "INT001",
            "road_A": road_A_data,
            "road_B": road_B_data,
            "pedestrian_A": {
                "walk_time": round(random.uniform(8, 13), 2),
                "do_not_walk_time": round(random.uniform(12, 18), 2),
                "clearance_time": round(random.uniform(6, 10), 2)
            },
            "pedestrian_B": {
                "walk_time": round(random.uniform(10, 15), 2),
                "do_not_walk_time": round(random.uniform(10, 15), 2),
                "clearance_time": round(random.uniform(5, 10), 2)
            }
        }

        date_key = current_time.strftime("%Y-%m-%d")
        if date_key not in data:
            data[date_key] = []
        
        data[date_key].append(entry)
        current_time += timedelta(minutes=interval_minutes)
    
    return data

# Define the start time, number of days, and interval
start_time = datetime(2021, 2, 15, 0, 0, 0)
num_days = 50  # Specify the number of days for data
interval_minutes = 30

# Generate the data
traffic_data = generate_traffic_data(start_time, num_days, interval_minutes)

# Save the data to a JSON file
with open('traffic_data.json', 'w') as file:
    json.dump(traffic_data, file, indent=4)

print("Traffic data has been saved to 'traffic_data.json'.")
