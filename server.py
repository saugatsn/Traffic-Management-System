from flask import Flask, jsonify, render_template
import random
import json

# app = Flask(__name__)

# # Function to generate random values for speed and volume
# def generate_random_data():
#     data = {
#         "road_A": {
#             "width": random.randint(10, 20),  # Width of road A in meters (random)
#             "speed": random.randint(30, 80),  # Speed of vehicles on road A (random)
#             "volume": random.randint(200, 400)  # Volume of vehicles on road A (random)
#         },
#         "road_B": {
#             "width": random.randint(10, 20),  # Width of road B in meters (random)
#             "speed": random.randint(30, 80),  # Speed of vehicles on road B (random)
#             "volume": random.randint(200, 400)  # Volume of vehicles on road B (random)
#         }
#     }
#     return data

# # Flask route to send the generated data to the frontend
# @app.route('/traffic-data')
# def traffic_data():
#     try:
#         data = generate_random_data()
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Flask route to render the HTML page
# @app.route('/')
# def index():
#     return render_template('index.html')  # This will load your HTML page

# if __name__ == '__main__':
#     app.run(debug=True)
