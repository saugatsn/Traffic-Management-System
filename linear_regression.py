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

    # Get the minute value
    minute = dt.minute

    # If the minute is 30 or more, round up to next hour
    if minute >= 30:
        dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        dt = dt.replace(minute=0, second=0, microsecond=0)
    
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

    # If less than 2 entries are found, use the last 20 data points
    if len(historical_data) < 2:
        for date, entries in traffic_data.items():
            for entry in entries[-20:]:  # Take last 20 data points
                historical_data.append(entry)

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

# Plot graphs for volumes and speeds
def plot_graph(dates, y, y_pred, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.scatter(dates, y, color='blue', label="Actual")
    plt.plot(dates, y_pred, color='red', label="Predicted")

    # Format x-axis with dates
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show one major tick every 6 months
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Show dates in the desired format
    plt.gcf().autofmt_xdate()  # Auto rotate date labels
    
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()

# Predict values for the next 24 hours
start_time = current_datetime
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

        # Print calculation steps
        print(f"\nCalculating for {prediction_time.strftime('%I:%M %p')}:")
        print(f"Date ordinal for prediction: {prediction_date_ordinal}")
        print(f"Predicted Volume for Road A: {predicted_volume_A_now[0]}")
        print(f"Predicted Speed for Road A: {predicted_speed_A_now[0]}")
        print(f"Predicted Volume for Road B: {predicted_volume_B_now[0]}")
        print(f"Predicted Speed for Road B: {predicted_speed_B_now[0]}")

        # Only plot the graph for the first hour (initial hour after rounding)
        if i == 0:
            predicted_volume_A = volume_A_model.predict(np.array([d.toordinal() for d in dates]).reshape(-1, 1))
            predicted_speed_A = speed_A_model.predict(np.array([d.toordinal() for d in dates]).reshape(-1, 1))
            predicted_volume_B = volume_B_model.predict(np.array([d.toordinal() for d in dates]).reshape(-1, 1))
            predicted_speed_B = speed_B_model.predict(np.array([d.toordinal() for d in dates]).reshape(-1, 1))
            
            # Plot graphs for the first hour predictions
            plot_graph(dates, volumes_A, predicted_volume_A, f"Road A - Vehicle Volumes at {prediction_time.strftime('%I:%M %p')}", "Volume")
            plot_graph(dates, speeds_A, predicted_speed_A, f"Road A - Vehicle Speeds at {prediction_time.strftime('%I:%M %p')}", "Speed")
            plot_graph(dates, volumes_B, predicted_volume_B, f"Road B - Vehicle Volumes at {prediction_time.strftime('%I:%M %p')}", "Volume")
            plot_graph(dates, speeds_B, predicted_speed_B, f"Road B - Vehicle Speeds at {prediction_time.strftime('%I:%M %p')}", "Speed")
