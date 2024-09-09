import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Define parameters
roads = ['Road A', 'Road B', 'Road C', 'Road D', 'Road E']
time_intervals = ['6:00-7:00', '7:00-8:00', '8:00-9:00', '9:00-10:00', '10:00-11:00', 
                  '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00']

# Simulate traffic data
traffic_data = []
for road in roads:
    for time in time_intervals:
        # Simulate the number of cars on each road at different times
        cars = random.randint(50, 500)  # Random number of cars
        traffic_data.append([road, time, cars])

# Create a DataFrame for traffic data
df_traffic = pd.DataFrame(traffic_data, columns=['Road', 'Time Interval', 'Number of Cars'])

# Save the data to a CSV file
df_traffic.to_csv('simulated_traffic_data.csv', index=False)

# Display the data
print(df_traffic)

# Load the simulated traffic data from Step 1
df_traffic = pd.read_csv('simulated_traffic_data.csv')

# Calculate the average number of cars per road
average_traffic_per_road = df_traffic.groupby('Road')['Number of Cars'].mean()

# Calculate the peak times (time intervals with maximum cars) for each road
peak_times_per_road = df_traffic.loc[df_traffic.groupby('Road')['Number of Cars'].idxmax()]

# Plot the average traffic per road
plt.figure(figsize=(8, 6))
average_traffic_per_road.plot(kind='bar', color='skyblue')
plt.title('Average Number of Cars per Road')
plt.xlabel('Road')
plt.ylabel('Average Number of Cars')
plt.xticks(rotation=0)
plt.show()

# Plot traffic trends over time for each road
plt.figure(figsize=(10, 8))
for road in df_traffic['Road'].unique():
    road_data = df_traffic[df_traffic['Road'] == road]
    plt.plot(road_data['Time Interval'], road_data['Number of Cars'], label=road)

plt.title('Traffic Trends Over Time')
plt.xlabel('Time Interval')
plt.ylabel('Number of Cars')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Display peak times for each road
print("Peak Times for Each Road:")
print(peak_times_per_road[['Road', 'Time Interval', 'Number of Cars']])


# Load the simulated traffic data
df_traffic = pd.read_csv('simulated_traffic_data.csv')

# Convert time intervals into numerical values (e.g., '6:00-7:00' -> 6)
df_traffic['Time Numeric'] = df_traffic['Time Interval'].apply(lambda x: int(x.split(':')[0]))

# Separate features (time) and target (number of cars)
X = df_traffic[['Time Numeric']]  # Feature: time of day
y = df_traffic['Number of Cars']  # Target: number of cars

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Visualize the predictions vs actual data
plt.figure(figsize=(8, 6))
plt.scatter(X_test, y_test, color='blue', label='Actual Traffic')
plt.plot(X_test, y_pred, color='red', label='Predicted Traffic')
plt.title('Predicted vs Actual Traffic')
plt.xlabel('Time of Day (hour)')
plt.ylabel('Number of Cars')
plt.legend()
plt.show()

# Evaluate the model (R^2 score)
r2_score = model.score(X_test, y_test)
print(f"Model R^2 Score: {r2_score:.2f}")

# Example prediction: Predict traffic for a specific time
example_time = np.array([[14]])  # 14:00 (2:00 PM)
predicted_traffic = model.predict(example_time)
print(f"Predicted traffic at 14:00: {predicted_traffic[0]:.0f} cars")

# Example thresholds for controlling traffic light timings (in seconds)
BASE_GREEN_TIME = 30  # Base green light time in seconds
MAX_GREEN_TIME = 60   # Maximum green light time for heavy traffic
MIN_GREEN_TIME = 10   # Minimum green light time for light traffic
TRAFFIC_THRESHOLD_HIGH = 400  # Number of cars considered as high traffic
TRAFFIC_THRESHOLD_LOW = 100   # Number of cars considered as low traffic

# Simulated predictions for each road and time (based on the prediction model from Step 3)
predicted_traffic = {
    'Road A': 350,  # Medium traffic
    'Road B': 500,  # Heavy traffic
    'Road C': 90,   # Light traffic
    'Road D': 450,  # Heavy traffic
    'Road E': 150   # Low-medium traffic
}

# Function to adjust green light time based on predicted traffic
def adjust_green_light(predicted_cars):
    if predicted_cars > TRAFFIC_THRESHOLD_HIGH:
        return MAX_GREEN_TIME  # Heavy traffic, increase green light time
    elif predicted_cars < TRAFFIC_THRESHOLD_LOW:
        return MIN_GREEN_TIME  # Light traffic, decrease green light time
    else:
        # Medium traffic, set green light based on proportion of traffic
        return int(BASE_GREEN_TIME + (predicted_cars - TRAFFIC_THRESHOLD_LOW) /
                   (TRAFFIC_THRESHOLD_HIGH - TRAFFIC_THRESHOLD_LOW) * (MAX_GREEN_TIME - BASE_GREEN_TIME))

# Create a dictionary to store the green light durations for each road
traffic_light_timings = {}

# Calculate green light timings for each road based on the predicted traffic
for road, traffic in predicted_traffic.items():
    green_light_time = adjust_green_light(traffic)
    traffic_light_timings[road] = green_light_time

# Display the green light timings for each road
print("Traffic Light Timings (in seconds):")
for road, time in traffic_light_timings.items():
    print(f"{road}: {time} seconds green light")