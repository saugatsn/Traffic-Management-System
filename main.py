import threading
import matplotlib.pyplot as plt
import random
import json
import time
from datetime import datetime, timedelta
import math

# Function to generate random values for speed and volume
def generate_random_data():
    current_hour = datetime.now().hour
    if (8 <= current_hour <= 11) or (16 <= current_hour <= 19):
        return {
            "width_A": random.randint(10, 20),
            "speed_A": random.randint(10, 40),
            "volume_A": random.randint(200, 400),
            "width_B": random.randint(10, 20),
            "speed_B": random.randint(10, 40),
            "volume_B": random.randint(200, 400)
        }
    else:
        return {
            "width_A": random.randint(10, 20),
            "speed_A": random.randint(40, 80),
            "volume_A": random.randint(50, 200),
            "width_B": random.randint(10, 20),
            "speed_B": random.randint(40, 80),
            "volume_B": random.randint(50, 200)
        }

# Step 1: Calculate Amber Time
def amber_time(speed):
    if speed <= 50:
        return 3
    elif speed <= 60:
        return 4
    else:
        return 5

# Step 2: Calculate Pedestrian Clearance Time
def pedestrian_clearance_time(road_width, pedestrian_speed=1.2):
    return road_width / pedestrian_speed

# Step 3: Calculate Minimum Red Light Time (based on pedestrian clearance)
def min_red_time(pedestrian_clearance_time):
    return pedestrian_clearance_time + 7

# Step 4: Calculate Actual Red Light Time (minimum red time + amber time)
def actual_red_time(min_red_time, amber_time):
    return min_red_time + amber_time

# Step 5: Calculate Minimum Green Time
def minimum_green_time(opposite_red_time, amber_time):
    return opposite_red_time - amber_time

# Step 6: Calculate Actual Green Time
def actual_green_time(min_green_A, min_green_B, volume_A, volume_B):
    if volume_A > volume_B:
        green_B = min_green_B
        green_A = (green_B * volume_A) / volume_B
    elif volume_B > volume_A:
        green_A = min_green_A
        green_B = (green_A * volume_B) / volume_A
    else: 
        green_A = min_green_A
        green_B = min_green_B
    return green_A, green_B

# Step 7: Calculate Cycle Length
def cycle_length(green_A, green_B, amber_A, amber_B):
    return green_A + green_B + amber_A + amber_B

# Step 8: Calculate "Do Not Walk" Time for Road A (using actual red time of Road B)
def do_not_walk_time_A(actual_red_B):
    return actual_red_B

def do_not_walk_time_B(actual_red_A):
    return actual_red_A    

# Step 9: Calculate Pedestrian Walk Time for Road A
def pedestrian_walk_time(cycle_length, do_not_walk_A, clearance_A):
    return cycle_length - do_not_walk_A - clearance_A

# New function to calculate the average of a list
def calculate_average(data_list):
    return sum(data_list) / len(data_list) if data_list else 0

# New function to get the representative time for the current period
def get_representative_time(current_time):
    if current_time.minute < 15:
        return current_time.replace(minute=0, second=0, microsecond=0)
    elif current_time.minute < 45:
        return current_time.replace(minute=30, second=0, microsecond=0)
    else:
        return (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

# Function to load existing data from JSON file
import json
import os

def load_existing_data():
    filename = 'traffic_data.json'
    
    if not os.path.exists(filename):
        # File doesn't exist, create it and return an empty dictionary
        with open(filename, 'w') as json_file:
            json.dump({}, json_file)
        return {}
    
    # File exists, try to read it
    with open(filename, 'r') as json_file:
        content = json_file.read()
        if not content:
            # File is empty, return an empty dictionary
            return {}
        else:
            # File has content, parse and return it
            return json.loads(content)


def save_data_to_json(data):
    filename = 'traffic_data.json'
    
    # Load existing data
    existing_data = load_existing_data()
    
    # Merge new data with existing data
    for date, entries in data.items():
        if date not in existing_data:
            existing_data[date] = []
        existing_data[date].extend(entries)
    
    # Write merged data back to file
    with open(filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
    print(f"Data has been appended to {filename}")

# Initialize arrays to store data for averaging
road_A_data = {'volume': [], 'speed': [], 'amber': [], 'red': [], 'green': [], 'walk': [], 'clearance': [], 'do_not_walk': []}
road_B_data = {'volume': [], 'speed': [], 'amber': [], 'red': [], 'green': [], 'walk': [], 'clearance': [], 'do_not_walk': []}

# Load existing data
traffic_data = load_existing_data()

while True:
    current_time = datetime.now()
    
    # Determine the start of the next cycle
    if current_time.minute < 15:
        next_cycle_start = current_time.replace(minute=15, second=0, microsecond=0)
    elif current_time.minute < 45:
        next_cycle_start = current_time.replace(minute=45, second=0, microsecond=0)
    else:
        next_cycle_start = (current_time + timedelta(hours=1)).replace(minute=15, second=0, microsecond=0)
    
    # Calculate time until next cycle
    time_to_next_cycle = (next_cycle_start - current_time).total_seconds()
    
    # Get the representative time for this period
    representative_time = get_representative_time(current_time)
    
    # Main simulation loop
    while (datetime.now() - current_time).total_seconds() < time_to_next_cycle:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        intersection_id = "INT001"
        road_A_id = "RA001"
        road_B_id = "RB001"

        # Generate and process traffic data
        traffic_data_random = generate_random_data()

        # Extract data for roads A and B
        width_A = traffic_data_random['width_A']
        speed_A = traffic_data_random['speed_A']
        volume_A = traffic_data_random['volume_A']

        width_B = traffic_data_random['width_B']
        speed_B = traffic_data_random['speed_B']
        volume_B = traffic_data_random['volume_B']
        
        print(f"For Road A: Width:{width_A} Speed:{speed_A} Volume:{volume_A} ")
        print(f"For Road B: Width:{width_B} Speed:{speed_B} Volume:{volume_B} ")

        # Perform Calculations
        amber_A = amber_time(speed_A)
        print(f"Amber Time for Road A: {amber_A} seconds")

        amber_B = amber_time(speed_B)
        print(f"Amber Time for Road B: {amber_B} seconds")

        clearance_A = pedestrian_clearance_time(width_A)
        print(f"Pedestrian Clearance Time for Road A: {clearance_A:.2f} seconds")

        clearance_B = pedestrian_clearance_time(width_B)
        print(f"Pedestrian Clearance Time for Road B: {clearance_B:.2f} seconds")

        # Minimum red light times (based on pedestrian clearance time)
        min_red_A = min_red_time(clearance_A)
        print(f"Minimum Red Light Time for Road A: {min_red_A:.2f} seconds")

        min_red_B = min_red_time(clearance_B)
        print(f"Minimum Red Light Time for Road B: {min_red_B:.2f} seconds")

        min_green_A = minimum_green_time(min_red_B, amber_A)
        print(f"Minimum Green Time for Road A: {min_green_A:.2f} seconds")

        min_green_B = minimum_green_time(min_red_A, amber_B)
        print(f"Minimum Green Time for Road B: {min_green_B:.2f} seconds")

        green_A_without_correction, green_B_without_correction = actual_green_time(min_green_A, min_green_B, volume_A, volume_B)
        print(f"Green Time without correction for Road A: {green_A_without_correction:.2f} seconds")
        print(f"Green Time without correction for Road B: {green_B_without_correction:.2f} seconds")

        cycle_len_without_round = cycle_length(green_A_without_correction, green_B_without_correction, amber_A, amber_B)
        cycle_len = math.ceil(cycle_len_without_round)
        discrepancy = cycle_len - cycle_len_without_round
        print(f"Cycle Length before correction: {cycle_len_without_round:.2f} seconds")
        print(f"Cycle Length after correction: {cycle_len:.2f} seconds")

        green_A = green_A_without_correction + (volume_A / (volume_A + volume_B)) * discrepancy
        green_B = green_B_without_correction + (volume_B / (volume_A + volume_B)) * discrepancy

        print(f"Corrected Green Time for Road A: {green_A:.2f} seconds")
        print(f"Corrected Green Time for Road B: {green_B:.2f} seconds")

        # Actual red light times (minimum red time + amber time)
        actual_red_A = actual_red_time(green_B, amber_B)
        print(f"Actual Red Light Time for Road A: {actual_red_A:.2f} seconds")

        actual_red_B = actual_red_time(green_A, amber_A)
        print(f"Actual Red Light Time for Road B: {actual_red_B:.2f} seconds")

        print("*" * 100)

        # Calculate the "Do Not Walk" time for road A (based on actual red time of road B)
        do_not_walk_A = do_not_walk_time_A(actual_red_B)
        print(f"Do Not Walk Time for Road A: {do_not_walk_A:.2f} seconds")

        do_not_walk_B = do_not_walk_time_B(actual_red_A)
        print(f"Do Not Walk Time for Road B: {do_not_walk_B:.2f} seconds")

        # Calculate the pedestrian walk time for road A and road B
        walk_A = pedestrian_walk_time(cycle_len, do_not_walk_A, clearance_A)
        print(f"Pedestrian Walk Time for Road A: {walk_A:.2f} seconds")

        walk_B = pedestrian_walk_time(cycle_len, do_not_walk_B, clearance_B)
        print(f"Pedestrian Walk Time for Road B: {walk_B:.2f} seconds")

        # Adjust the pedestrian walk time and clearance time if necessary to ensure it fits within one cycle
        if walk_A + clearance_A + do_not_walk_A > cycle_len:
            walk_A = cycle_len - clearance_A - do_not_walk_A
        if walk_B + clearance_B + do_not_walk_B > cycle_len:
            walk_B = cycle_len - clearance_B - do_not_walk_B

        print("*" * 100)

        print(f"TSA Green Time: {green_A:.2f} seconds, Amber Time: {amber_A:.2f} seconds, Red Time: {actual_red_A:.2f} seconds")
        print(f"PSB Walk Time: {walk_B:.2f} seconds, Clearance Time: {clearance_B:.2f} seconds, Do Not Walk Time: {do_not_walk_B:.2f} seconds")

        print(f"TSB Green Time: {green_B:.2f} seconds, Amber Time: {amber_B:.2f} seconds, Red Time: {actual_red_B:.2f} seconds")
        print(f"PSA Walk Time: {walk_A:.2f} seconds, Clearance Time: {clearance_A:.2f} seconds, Do Not Walk Time: {do_not_walk_A:.2f} seconds")

        print(f"Total time for road A: {green_A + actual_red_A + amber_A}")
        print(f"Total time for road B: {green_B + actual_red_B + amber_B}")
        print(f"Total time for pedestrian in road A in 1 cycle: {walk_A + clearance_A + do_not_walk_A}")
        print(f"Total time for pedestrian in road B in 1 cycle: {walk_B + clearance_B + do_not_walk_B}")

        print("*" * 100)

        # Append data to the arrays
        road_A_data['volume'].append(volume_A)
        road_A_data['speed'].append(speed_A)
        road_A_data['amber'].append(amber_A)
        road_A_data['red'].append(actual_red_A)
        road_A_data['green'].append(green_A)
        road_A_data['walk'].append(walk_A)
        road_A_data['clearance'].append(clearance_A)
        road_A_data['do_not_walk'].append(do_not_walk_A)

        road_B_data['volume'].append(volume_B)
        road_B_data['speed'].append(speed_B)
        road_B_data['amber'].append(amber_B)
        road_B_data['red'].append(actual_red_B)
        road_B_data['green'].append(green_B)
        road_B_data['walk'].append(walk_B)
        road_B_data['clearance'].append(clearance_B)
        road_B_data['do_not_walk'].append(do_not_walk_B)

        print("Road A data array:")
        print(road_A_data)
        print("Road B data array:")
        print(road_B_data)
        print("*"*100)

        # Visualize the Results
        fig, ax = plt.subplots(2, 1, figsize=(10, 6))  # 2 rows, 1 column

        # TSA and PSB visualization (Start with Green -> Yellow -> Red)
        bar1 = ax[0].barh(['PSB'], [walk_B], color='#32CD32', label='Walk')  # Lighter green for PSB
        bar2 = ax[0].barh(['PSB'], [clearance_B], left=[walk_B], color='#FFD700', label='Clearance')  # Different yellow
        bar3 = ax[0].barh(['PSB'], [do_not_walk_B], left=[walk_B + clearance_B], color='#FF6347', label='Do Not Walk')  # Faded red

        bar4 = ax[0].barh(['TSA'], [green_A], color='#228B22', label='Green')  # Darker green for TSA
        bar5 = ax[0].barh(['TSA'], [amber_A], left=[green_A], color='yellow', label='Amber')
        bar6 = ax[0].barh(['TSA'], [actual_red_A], left=[green_A + amber_A], color='red', label='Red')

        # Customizing the legend for TSA and PSB
        handles, labels = ax[0].get_legend_handles_labels()
        order = [3, 4, 5, 0, 1, 2]  # Custom order: Green -> Amber -> Red -> Walk -> Clearance -> Do Not Walk
        ax[0].legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper right', bbox_to_anchor=(1.15, 1))
        ax[0].set_title('TSA and PSB')

        # TSB and PSA visualization (Start with Red -> Green -> Yellow)
        bar7 = ax[1].barh(['PSA'], [do_not_walk_A], color='#FF6347', label='Do Not Walk')  # Faded red for PSA
        bar8 = ax[1].barh(['PSA'], [walk_A], left=[do_not_walk_A], color='#32CD32', label='Walk')  # Lighter green
        bar9 = ax[1].barh(['PSA'], [clearance_A], left=[do_not_walk_A + walk_A], color='#FFD700', label='Clearance')  # Yellow for clearance

        bar10 = ax[1].barh(['TSB'], [actual_red_B], color='red', label='Red')
        bar11 = ax[1].barh(['TSB'], [green_B], left=[actual_red_B], color='#228B22', label='Green')  # Darker green for TSB
        bar12 = ax[1].barh(['TSB'], [amber_B], left=[actual_red_B + green_B], color='yellow', label='Amber')  # Yellow after green

        # Customizing the legend for TSB and PSA
        handles, labels = ax[1].get_legend_handles_labels()
        order = [3, 4, 5, 0, 1, 2]  # Custom order: Do Not Walk -> Clearance -> Walk -> Red -> Amber -> Green
        ax[1].legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper right', bbox_to_anchor=(1.15, 1))
        ax[1].set_title('TSB and PSA')

        plt.tight_layout()
        plt.show(block=False)  # Make sure the plot doesn't block the cycle

        # Use plt.pause to simulate the cycle
        start_time = time.time()
        elapsed = 0

        # Run until the cycle length is over, regardless of window closure
        while elapsed < cycle_len:
            elapsed = time.time() - start_time
            plt.pause(0.1)  # Keep updating the graph until the cycle length ends

        # Now the cycle is over, we proceed to the next iteration
        plt.close()  # Close the plot after the full cycle is done

    # Calculate and print averages
    print(f"Averages for period {representative_time}:")
    road_A_avg = {}
    road_B_avg = {}
    print("Road A:")
    for key, values in road_A_data.items():
        avg = calculate_average(values)
        road_A_avg[key] = avg
        print(f"  Average {key}: {avg:.2f}")

    print("Road B:")
    for key, values in road_B_data.items():
        avg = calculate_average(values)
        road_B_avg[key] = avg
        print(f"  Average {key}: {avg:.2f}")

    # Prepare data for JSON
    date_key = representative_time.strftime("%Y-%m-%d")
    new_data = {
        "timestamp": representative_time.strftime("%Y-%m-%d %H:%M:%S"),
        "intersection_id": intersection_id,
        "road_A": {
            "road_id": road_A_id,
            "vehicle_count": int(road_A_avg['volume']),
            "avg_speed": int(road_A_avg['speed']),
            "green_time": road_A_avg['green'],
            "red_time": road_A_avg['red'],
            "amber_time": road_A_avg['amber']
        },
        "road_B": {
            "road_id": road_B_id,
            "vehicle_count": int(road_B_avg['volume']),
            "avg_speed": int(road_B_avg['speed']),
            "green_time": road_B_avg['green'],
            "red_time": road_B_avg['red'],
            "amber_time": road_B_avg['amber']
        },
        "pedestrian_A": {
            "walk_time": road_A_avg['walk'],
            "do_not_walk_time": road_A_avg['do_not_walk'],
            "clearance_time": road_A_avg['clearance']
        },
        "pedestrian_B": {
            "walk_time": road_B_avg['walk'],
            "do_not_walk_time": road_B_avg['do_not_walk'],
            "clearance_time": road_B_avg['clearance']
        }
    }

    # Add new data to existing data
    if date_key not in traffic_data:
        traffic_data[date_key] = []
    traffic_data[date_key].append(new_data)

    # Save updated data to JSON file
    save_data_to_json(traffic_data)
    print(f"Data for {representative_time} has been appended to traffic_data.json")

    # Clear the data arrays for the next cycle
    for data in [road_A_data, road_B_data]:
        for key in data:
            data[key] = []

    print("Starting next cycle...")
    print("=" * 100)