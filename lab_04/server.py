from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import ssl
import sys

app = Flask(__name__)

# загрузка ключа Fernet
with open("encryption_key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# хранилище сообщений
user_messages = []

@app.route("/api/data", methods=["POST"])
def handle():

    encrypted = request.json["data"]

    try:
        decrypted = fernet.decrypt(
            encrypted.encode()
        ).decode()

        print("Получено:", decrypted)

        user_messages.append({
            "id": len(user_messages) + 1,
            "message": decrypted
        })

        return jsonify({
            "status": "ok",
            "message": decrypted
        })

    except:
        return jsonify({
            "error": "decryption failed"
        }), 400

@app.route("/messages", methods=["GET"])
def get_messages():

    sort_order = request.args.get(
        "sort",
        "asc"
    )

    sorted_messages = sorted(
        user_messages,
        key=lambda x: x["message"],
        reverse=(sort_order == "desc")
    )

    return jsonify(sorted_messages)

if __name__ == "__main__":

    port = int(sys.argv[1])

    context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER
    )

    context.load_cert_chain(
        "server_cert.pem",
        "server_key.pem"
    )

    context.load_verify_locations(
        "ca_cert.pem"
    )

    context.verify_mode = ssl.CERT_REQUIRED

    app.run(
        host="0.0.0.0",
        port=port,
        ssl_context=context
    )
