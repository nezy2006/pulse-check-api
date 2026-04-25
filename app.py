import threading
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

monitors = {}

@app.route('/')
def home():
    return "Pulse Check API is running"


@app.route('/monitors', methods=['POST'])
def register_monitor():
    data = request.get_json()

    device_id = data['id']
    timeout = data['timeout']

    monitors[device_id] = {
        "timeout": timeout,
        "last_ping": time.time(),
        "status": "active"
    }

    return jsonify({
        "message": f"Monitor {device_id} registered",
        "data": monitors[device_id]
    }), 201


@app.route('/monitors', methods=['GET'])
def get_monitors():
    return jsonify(monitors), 200


@app.route('/monitors/<device_id>/heartbeat', methods=['POST'])
def heartbeat(device_id):
    if device_id not in monitors:
        return jsonify({"error": "Monitor not found"}), 404

    monitors[device_id]["last_ping"] = time.time()
    monitors[device_id]["status"] = "active"

    return jsonify({
        "message": f"Heartbeat received from {device_id}",
        "data": monitors[device_id]
    }), 200


def check_monitors():
    while True:
        current_time = time.time()

        for device_id, data in monitors.items():
            last_ping = data["last_ping"]
            timeout = data["timeout"]

            if last_ping and (current_time - last_ping > timeout) and data["status"] != "down":
                alert = {
                    "ALERT": f"Device {device_id} is down!",
                    "time": current_time
                }
                print(alert)
                data["status"] = "down"

        time.sleep(5)


if __name__ == '__main__':
    thread = threading.Thread(target=check_monitors)
    thread.daemon = True
    thread.start()

    app.run(debug=True)