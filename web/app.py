#!/usr/bin/python
import os
import shlex
import subprocess

from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

HOST = os.environ.get("WGMETRICS_HOST", "0.0.0.0")
PORT = int(os.environ.get("WGMETRICS_PORT", 8000))

@app.route("/wgmetrics", methods=["GET"])
def get_metrics():
    interface = request.args.get("interface")
    command = ["wg", "show", shlex.quote(f"{interface}"), "dump"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify(error="Failed to get metrics"), 500

    output = result.stdout.strip().split("\n")

    metrics = []

    for line in output:
        fields = line.strip().split()
        if len(fields) < 6:
            continue
        metrics.append({
            "interface": interface,
            "public_key": fields[0],
            "endpoint": fields[2],
            "allowed_ips": fields[3],
            "handshake": fields[4],
            "data": {
                "received": fields[5],
                "sent": fields[6]
            }
        })

    return jsonify(metrics)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = jsonify(error=str(e))
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
