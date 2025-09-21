from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# You can keep your core logic in a class or just as functions
class ParkingSimulator:
    def __init__(self, total_spots=20):
        self.total_spots = total_spots
        self.parking_spots = {}
        self.initialize_spots()

    def initialize_spots(self):
        for i in range(1, self.total_spots + 1):
            self.parking_spots[i] = "Available"
        self.update_spots()

    def update_spots(self):
        for spot in self.parking_spots:
            if random.random() > 0.5:
                self.parking_spots[spot] = "Occupied"
            else:
                self.parking_spots[spot] = "Available"
        # Simulate a delay for a real-time feel
        time.sleep(0.5)

    def get_status(self):
        available_count = sum(1 for status in self.parking_spots.values() if status == "Available")
        return {
            "total_spots": self.total_spots,
            "available_spots": available_count,
            "spots": self.parking_spots
        }

simulator = ParkingSimulator()

@app.route('/')
def index():
    """Renders the main web page for the app."""
    return render_template('index.html')

@app.route('/api/status')
def get_status_api():
    """API endpoint to get the current parking status."""
    return jsonify(simulator.get_status())

@app.route('/api/refresh')
def refresh_api():
    """API endpoint to refresh the parking status."""
    simulator.update_spots()
    return jsonify({"message": "Refreshed"})

if __name__ == '__main__':
    app.run(debug=True)