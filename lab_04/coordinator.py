from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

servers = [
    "https://localhost:5001",
    "https://localhost:5002"
]

@app.route("/api/data", methods=["POST"])
def proxy():

    for server in servers:

        try:

            resp = requests.post(
                server + "/api/data",
                json=request.json,
                cert=(
                    "client_cert.pem",
                    "client_key.pem"
                ),
                verify=False
            )

            return jsonify(
                resp.json()
            )

        except:

            print(
                "Server failed:",
                server
            )

    return jsonify({
        "error": "all servers down"
    }), 500

@app.route("/messages", methods=["GET"])
def messages():

    for server in servers:

        try:

            resp = requests.get(
                server + "/messages",
                params=request.args,
                cert=(
                    "client_cert.pem",
                    "client_key.pem"
                ),
                verify=False
            )

            return jsonify(
                resp.json()
            )

        except:

            continue

    return jsonify({
        "error": "all servers down"
    }), 500

if __name__ == "__main__":
    app.run(port=8000)
