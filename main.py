import matplotlib.pyplot as plt

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

# Input Data
width_A = 18  # Width of road A in meters
width_B = 12  # Width of road B in meters
speed_A = 55  # Approach speed of vehicles on road A in km/h
speed_B = 40  # Approach speed of vehicles on road B in km/h
volume_A = 275  # Average approach volume per hour for road A
volume_B = 225  # Average approach volume per hour for road B

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

green_A, green_B = actual_green_time(min_green_A, min_green_B, volume_A, volume_B)
print(f"Actual Green Time for Road A: {green_A:.2f} seconds")
print(f"Actual Green Time for Road B: {green_B:.2f} seconds")

cycle_len = cycle_length(green_A, green_B, amber_A, amber_B)
print(f"Cycle Length: {cycle_len:.2f} seconds")

# Actual red light times (minimum red time + amber time)
actual_red_A = actual_red_time(green_B, amber_B)
print(f"Actual Red Light Time for Road A: {actual_red_A:.2f} seconds")

actual_red_B = actual_red_time(green_A, amber_A)
print(f"Actual Red Light Time for Road B: {actual_red_B:.2f} seconds")

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

print(f"TSA Green Time: {green_A:.2f} seconds, Amber Time: {amber_A:.2f} seconds, Red Time: {actual_red_A:.2f} seconds")
print(f"PSB Walk Time: {walk_B:.2f} seconds, Clearance Time: {clearance_B:.2f} seconds, Do Not Walk Time: {do_not_walk_B:.2f} seconds")

print(f"TSB Green Time: {green_B:.2f} seconds, Amber Time: {amber_B:.2f} seconds, Red Time: {actual_red_B:.2f} seconds")
print(f"PSA Walk Time: {walk_A:.2f} seconds, Clearance Time: {clearance_A:.2f} seconds, Do Not Walk Time: {do_not_walk_A:.2f} seconds")


# Visualize the Results
fig, ax = plt.subplots(2, 1, figsize=(10, 6))  # 2 rows, 1 column

# TSA and PSB visualization (Start with Green -> Yellow -> Red)
bar1 = ax[0].barh(['PSB'], [walk_B], color='#32CD32', label='Walk')  # Lighter green for PSB
bar2 = ax[0].barh(['PSB'], [clearance_B], left=[walk_B], color='#FFD700', label='Clearance')  # Different yellow
bar3 = ax[0].barh(['PSB'], [do_not_walk_B], left=[walk_B + clearance_B], color='#FF6347', label='Do Not Walk')  # Faded red

bar4 = ax[0].barh(['TSA'], [green_A], color='#228B22', label='Green')  # Darker green for TSA
bar5 = ax[0].barh(['TSA'], [amber_A], left=[green_A], color='yellow', label='Amber')
bar6 = ax[0].barh(['TSA'], [min_red_A], left=[green_A + amber_A], color='red', label='Red')

# Customizing the legend for TSA and PSB
handles, labels = ax[0].get_legend_handles_labels()
order = [3, 4, 5, 0, 1, 2]  # Custom order: Green -> Amber -> Red -> Walk -> Clearance -> Do Not Walk
ax[0].legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper right', bbox_to_anchor=(1.15, 1))
ax[0].set_title('TSA and PSB')

# TSB and PSA visualization (Start with Red -> Yellow -> Green)
bar7 = ax[1].barh(['PSA'], [do_not_walk_A], color='#FF6347', label='Do Not Walk')  # Faded red for PSA
bar8 = ax[1].barh(['PSA'], [clearance_A], left=[do_not_walk_A], color='#FFD700', label='Clearance')  # Different yellow
bar9 = ax[1].barh(['PSA'], [walk_A], left=[do_not_walk_A + clearance_A], color='#32CD32', label='Walk')  # Lighter green

bar10 = ax[1].barh(['TSB'], [actual_red_B], color='red', label='Red')
bar11 = ax[1].barh(['TSB'], [amber_B], left=[actual_red_B], color='yellow', label='Amber')
bar12 = ax[1].barh(['TSB'], [green_B], left=[actual_red_B + amber_B], color='#228B22', label='Green')  # Darker green for TSB

# Customizing the legend for TSB and PSA
handles, labels = ax[1].get_legend_handles_labels()
order = [3, 4, 5, 0, 1, 2]  # Custom order: Do Not Walk -> Clearance -> Walk -> Red -> Amber -> Green
ax[1].legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper right', bbox_to_anchor=(1.15, 1))
ax[1].set_title('TSB and PSA')

plt.tight_layout()
plt.show()
