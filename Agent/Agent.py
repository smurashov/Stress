import psutil
import Collector
import os
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start_monitor():
    Collector.start()
    return jsonify({'status': 'success'})

@app.route('/stop', methods=['GET'])
def stop_monitor():
    Collector.stop()
    return jsonify({'status': 'success'})

@app.route('/metrics', methods=['GET'])
def get_metrics():
    file_name = 'metrics.txt'
    path = os.getcwd()
    return send_from_directory(path, file_name)


if __name__ == '__main__':
    app.run(debug=True, port=7007, host='0.0.0.0')
