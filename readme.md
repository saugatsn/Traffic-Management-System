# Traffic Prediction and Signal Optimization

This project aims to optimize traffic signal timing and predict traffic conditions using real-time data analysis and linear regression model.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

## Overview

This repository contains a system that:

1. Calculates traffic cycle length at an intersection
2. Adjusts signal timing based on current traffic conditions
3. Uses a linear regression model to predict traffic conditions for the next 24 hours

## Features

- Dynamic traffic signal timing calculation
- Pedestrian and vehicle signal timing optimization
- Real-time traffic data processing
- 24-hour traffic condition prediction
- Visualization of signal timing

## How It Works

1. Due to lack of real sensor data, the system generates random speed and volume data, saving it to a JSON file.
2. `main.py` processes the JSON data to calculate optimal signal timing for both vehicles and pedestrians based on volume, speed, and road width.
3. The program generates plots to visualize the calculated timing.
4. `linear_regression.py` uses the accumulated data to fit a linear regression model, predicting traffic conditions for the next 24 hours.
5. The system runs for 30-minute intervals, after which it calculates average values for volume, speed, and signal timings. These averages are saved to `traffic_data.json`, and a new 24-hour prediction is made.
6. As more data is collected in `traffic_data.json`, the prediction accuracy improves over time.

## Installation

```bash
git clone https://github.com/yourusername/traffic-prediction.git
cd traffic-prediction
pip install -r requirements.txt
```

## Usage

1. Run the main program:

   ```
   python main.py
   ```

2. After accumulating some data, run the prediction model:
   ```
   python linear_regression.py
   ```

## Dependencies

Standard library:

- json
- datetime
- time
- math
- random
- threading

External libraries (specified in requirements.txt):

- matplotlib
- numpy
- scikit-learn

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
