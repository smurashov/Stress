import psutil
import Collector
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start_monitor():
    Collector.start()
    return jsonify({'status': 'success'})

@app.route('/stop', methods=['GET'])
def stop_monitor():
    Collector.stop()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, port=7007)
