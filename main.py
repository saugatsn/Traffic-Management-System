import threading
import matplotlib.pyplot as plt
import random
import json
import time
from datetime import datetime
import math

# Function to generate random values for speed and volume
def generate_random_data():
    # Get the current hour
    current_hour = datetime.now().hour

    # Peak hours: 8-11 AM and 4-7 PM
    if (8 <= current_hour <= 11) or (16 <= current_hour <= 19):
        # During peak hours, reduce speed and increase volume slightly
        data = {
            "road_A": {
                "width": random.randint(10, 20),  # Width of road A in meters (constant)
                "speed": random.randint(10, 40),  # Reduced speed during peak hours
                "volume": random.randint(200, 400)  # Increased volume during peak hours
            },
            "road_B": {
                "width": random.randint(10, 20),  # Width of road B in meters (constant)
                "speed": random.randint(10, 40),  # Reduced speed during peak hours
                "volume": random.randint(200, 400)  # Increased volume during peak hours
            }
        }
    else:
        # Non-peak hours, higher speed and lower volume
        data = {
            "road_A": {
                "width": random.randint(10, 20),  # Width of road A in meters (constant)
                "speed": random.randint(40, 80),  # Higher speed during non-peak hours
                "volume": random.randint(50, 200)  # Lower volume during non-peak hours
            },
            "road_B": {
                "width": random.randint(10, 20),  # Width of road B in meters (constant)
                "speed": random.randint(40, 80),  # Higher speed during non-peak hours
                "volume": random.randint(50, 200)  # Lower volume during non-peak hours
            }
        }
    return json.dumps(data, indent=4)

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

traffic_data_records = []
window_open=True
while True:
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Generate current timestamp
    intersection_id = "INT001"  # Example intersection ID
    road_A_id = "RA001"  # Road A ID
    road_B_id = "RB001"  # Road B ID

        # Get values from JSON
    traffic_data_json = generate_random_data()
    traffic_data = json.loads(traffic_data_json)

    # Extract the data for road A and B
    width_A = traffic_data['road_A']['width']
    speed_A = traffic_data['road_A']['speed']
    volume_A = traffic_data['road_A']['volume']

    width_B = traffic_data['road_B']['width']
    speed_B = traffic_data['road_B']['speed']
    volume_B = traffic_data['road_B']['volume']

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
    discrepancy= cycle_len-cycle_len_without_round
    print(f"Cycle Length before correction: {cycle_len_without_round:.2f} seconds")
    print(f"Cycle Length after correction: {cycle_len:.2f} seconds")


    green_A=green_A_without_correction+(volume_A/(volume_A+volume_B))*discrepancy
    green_B=green_B_without_correction+(volume_B/(volume_A+volume_B))*discrepancy
    

    print(f"Corrected Green Time for Road A: {green_A:.2f} seconds")
    print(f"Corrected Green Time for Road B: {green_B:.2f} seconds")

    # Actual red light times (minimum red time + amber time)
    actual_red_A = actual_red_time(green_B, amber_B)
    print(f"Actual Red Light Time for Road A: {actual_red_A:.2f} seconds")

    actual_red_B = actual_red_time(green_A, amber_A)
    print(f"Actual Red Light Time for Road B: {actual_red_B:.2f} seconds")

    print("*"*100)

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

    # Print the red, green, and amber times for road A (TSA) and road B (TSB)
    # Print the walk and clearance times for pedestrians on roads A and B (PSA and PSB)

    print("*"*100)

    print(f"TSA Green Time: {green_A:.2f} seconds, Amber Time: {amber_A:.2f} seconds, Red Time: {actual_red_A:.2f} seconds")
    print(f"PSB Walk Time: {walk_B:.2f} seconds, Clearance Time: {clearance_B:.2f} seconds, Do Not Walk Time: {do_not_walk_B:.2f} seconds")

    print(f"TSB Green Time: {green_B:.2f} seconds, Amber Time: {amber_B:.2f} seconds, Red Time: {actual_red_B:.2f} seconds")
    print(f"PSA Walk Time: {walk_A:.2f} seconds, Clearance Time: {clearance_A:.2f} seconds, Do Not Walk Time: {do_not_walk_A:.2f} seconds")

    print(f"Total time for road A: {green_A+actual_red_A+amber_A}")
    print(f"Total time for road B: {green_B+actual_red_B+amber_B}")
    print(f"Total time for pedestrian in road A in 1 cycle: {walk_A+clearance_A+do_not_walk_A}")
    print(f"Total time for pedestrian in road B in 1 cycle: {walk_B+clearance_B+do_not_walk_B}")

    print("*"*100)

        # Create a record for the current cycle
    record = {
        "timestamp": timestamp,
        "intersection_id": intersection_id,
        "road_A": {
            "road_id": road_A_id,
            "vehicle_count": volume_A,
            "avg_speed": speed_A,
            "green_time": green_A,
            "red_time": actual_red_A,
            "amber_time": amber_A
        },
        "road_B": {
            "road_id": road_B_id,
            "vehicle_count": volume_B,
            "avg_speed": speed_B,
            "green_time": green_B,
            "red_time": actual_red_B,
            "amber_time": amber_B
        },
        "pedestrian_A": {
            "walk_time": walk_A,
            "do_not_walk_time": do_not_walk_A,
            "clearance_time": clearance_A
        },
        "pedestrian_B": {
            "walk_time": walk_B,
            "do_not_walk_time": do_not_walk_B,
            "clearance_time": clearance_B
        }
    }

    # Append the record to the list
    traffic_data_records.append(record)
    # print(traffic_data_records)

    # Save the data to a JSON file after every cycle
    with open('traffic_data.json', 'w') as json_file:
        json.dump(traffic_data_records, json_file, indent=4)


    # Visualize the Results (unchanged from original code)
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
