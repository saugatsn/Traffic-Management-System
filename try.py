import json
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Function to round off time to nearest 30 minutes
def round_time(dt=None):
    """Round a datetime object to the nearest 30 minutes."""
    if dt is None:
        dt = datetime.now()

    # Get the number of minutes passed in the current hour
    minute = dt.minute

    # If the minutes are between 0 and 14, round down to the start of the hour
    if minute < 15:
        dt = dt.replace(minute=0, second=0, microsecond=0)
    # If the minutes are between 15 and 44, round to 30 minutes
    elif minute < 45:
        dt = dt.replace(minute=30, second=0, microsecond=0)
    # If the minutes are between 45 and 59, round up to the next hour
    else:
        dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    return dt

# Load traffic data from JSON
with open('traffic_data.json', 'r') as f:
    traffic_data = json.load(f)

# Get current date and rounded-off time
current_datetime = round_time(datetime.now())
current_date_str = current_datetime.strftime("%Y-%m-%d")

# Function to find historical data for a specific hour
def find_historical_data(traffic_data, target_time):
    target_time_str = target_time.strftime("%H:%M:%S")
    historical_data = []
    
    for date, entries in traffic_data.items():
        for entry in entries:
            # Check if the month and day match the target date
            if date[5:] == target_time.strftime("%m-%d") and entry['timestamp'].endswith(target_time_str):
                historical_data.append(entry)

    # If less than 2 entries are found, use the last 20 data points of the exact time
    if len(historical_data) < 2:
        exact_time_data = []
        for date, entries in traffic_data.items():
            for entry in entries:
                if entry['timestamp'].endswith(target_time_str):
                    exact_time_data.append(entry)
        historical_data = exact_time_data[-20:]  # Take last 20 data points of the exact time

    return historical_data

# Function to perform regression for a given hour
def perform_regression(historical_data):
    dates = []
    volumes_A = []
    speeds_A = []
    volumes_B = []
    speeds_B = []

    for data in historical_data:
        date_obj = datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")
        dates.append(date_obj)
        # Format dates in a more readable format
        formatted_dates = [d.strftime("%B %d, %Y, %I:%M %p") for d in dates]

        # Collect data for Road A and Road B
        volumes_A.append(data['road_A']['vehicle_count'])
        speeds_A.append(data['road_A']['avg_speed'])
        volumes_B.append(data['road_B']['vehicle_count'])
        speeds_B.append(data['road_B']['avg_speed'])

    # Convert lists to numpy arrays
    date_nums = np.array([d.toordinal() for d in dates]).reshape(-1, 1)
    volumes_A = np.array(volumes_A)
    speeds_A = np.array(speeds_A)
    volumes_B = np.array(volumes_B)
    speeds_B = np.array(speeds_B)

    # Print data for regression
    print(f"\nPerforming regression on historical data.")
    print(f"Dates: {formatted_dates}")
    print(f"Volumes A: {volumes_A}")
    print(f"Speeds A: {speeds_A}")
    print(f"Volumes B: {volumes_B}")
    print(f"Speeds B: {speeds_B}")

    # Perform linear regression for Road A and Road B volumes and speeds
    volume_A_model = LinearRegression().fit(date_nums, volumes_A)
    speed_A_model = LinearRegression().fit(date_nums, speeds_A)
    volume_B_model = LinearRegression().fit(date_nums, volumes_B)
    speed_B_model = LinearRegression().fit(date_nums, speeds_B)

    return volume_A_model, speed_A_model, volume_B_model, speed_B_model, dates, volumes_A, speeds_A, volumes_B, speeds_B

# Predict values for the next 24 hours and print them
def predict_traffic_for_24_hours():
    start_time = current_datetime
    traffic_predictions = []
    
    for i in range(24):
        prediction_time = start_time + timedelta(hours=i)
        
        # Fetch historical data for this hour
        historical_data = find_historical_data(traffic_data, prediction_time)
        
        # If we have data, perform regression and make predictions
        if historical_data:
            volume_A_model, speed_A_model, volume_B_model, speed_B_model, dates, volumes_A, speeds_A, volumes_B, speeds_B = perform_regression(historical_data)
            
            # Make predictions
            prediction_date_ordinal = np.array([[prediction_time.toordinal()]])
            
            predicted_volume_A_now = volume_A_model.predict(prediction_date_ordinal)
            predicted_speed_A_now = speed_A_model.predict(prediction_date_ordinal)
            predicted_volume_B_now = volume_B_model.predict(prediction_date_ordinal)
            predicted_speed_B_now = speed_B_model.predict(prediction_date_ordinal)

            traffic_predictions.append({
                'time': prediction_time.strftime('%I:%M %p'),
                'volume_A': predicted_volume_A_now[0],
                'speed_A': predicted_speed_A_now[0],
                'volume_B': predicted_volume_B_now[0],
                'speed_B': predicted_speed_B_now[0]
            })

            # Print the calculated predictions
            print(f"\nCalculating for {prediction_time.strftime('%I:%M %p')}:")
            print(f"Predicted Volume for Road A: {predicted_volume_A_now[0]}")
            print(f"Predicted Speed for Road A: {predicted_speed_A_now[0]}")
            print(f"Predicted Volume for Road B: {predicted_volume_B_now[0]}")
            print(f"Predicted Speed for Road B: {predicted_speed_B_now[0]}")

    return traffic_predictions

# Function to give insights based on traffic predictions
def provide_traffic_insights(traffic_predictions):
    print("\nTraffic Insights for the next 24 hours:")
    for prediction in traffic_predictions:
        time = prediction['time']
        volume_A = prediction['volume_A']
        speed_A = prediction['speed_A']
        volume_B = prediction['volume_B']
        speed_B = prediction['speed_B']

        # Simple logic for traffic insights
        if volume_A >= 400 and (speed_A >= 10 and speed_A <= 40):
            traffic_condition = "slow-moving and congested"
        elif volume_A >= 400 and (speed_A > 40):
            traffic_condition = "congested and fast-moving"
        elif volume_A < 200 and (speed_A >= 10 and speed_A <= 40):
            traffic_condition = "clear and slow-moving"
        elif volume_A < 200 and (speed_A > 40):
            traffic_condition = "clear and fast-moving"
        elif volume_A >= 200 and volume_A < 400 and (speed_A >= 10 and speed_A <= 40):
            traffic_condition = "moderate traffic and slow-moving"
        elif volume_A >= 200 and volume_A < 400 and (speed_A > 40):
            traffic_condition = "moderate traffic and fast-moving"
        else:
            traffic_condition = "unknown condition"
        
        print(f"FOR ROAD B: At {time}, the traffic is expected to be {traffic_condition}. "
              f"Road A: {int(volume_A)} vehicles, {int(speed_A)} km/h. "
              f"Road B: {int(volume_B)} vehicles, {int(speed_B)} km/h.")
        if volume_B >= 400 and (speed_B >= 10 and speed_B <= 40):
            traffic_condition = "slow-moving and congested"
        elif volume_B >= 400 and (speed_B > 40):
            traffic_condition = "congested and fast-moving"
        elif volume_B < 200 and (speed_B >= 10 and speed_B <= 40):
            traffic_condition = "clear and slow-moving"
        elif volume_B < 200 and (speed_B > 40):
            traffic_condition = "clear and fast-moving"
        elif volume_B >= 200 and volume_B < 400 and (speed_B >= 10 and speed_B <= 40):
            traffic_condition = "moderate traffic and slow-moving"
        elif volume_B >= 200 and volume_B < 400 and (speed_B > 40):
            traffic_condition = "moderate traffic and fast-moving"
        else:
            traffic_condition = "unknown condition"

        print(f"FOR ROAD A: At {time}, the traffic is expected to be {traffic_condition}. "
              f"Road A: {int(volume_A)} vehicles, {int(speed_A)} km/h. "
              f"Road B: {int(volume_B)} vehicles, {int(speed_B)} km/h.")

# Run the prediction and insights in a loop indefinitely
while True:
    traffic_predictions = predict_traffic_for_24_hours()
    provide_traffic_insights(traffic_predictions)

    # Wait until the next 30-minute rounded interval to re-run
    current_datetime = round_time(datetime.now())
    next_update_time = current_datetime + timedelta(minutes=30)
    
    while datetime.now() < next_update_time:
        pass  # Keep the program running