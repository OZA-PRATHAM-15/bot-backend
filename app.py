from flask import Flask, request, jsonify
from utils.db import get_database
from intents.analytics import handle_analytics_query 
from flask_cors import CORS
from waitress import serve
import os
from dotenv import load_dotenv

load_dotenv()
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
app = Flask(__name__)

CORS(app, origins=[frontend_origin] if frontend_origin != "*" else "*", supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = frontend_origin if frontend_origin != "*" else "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route('/bot-api/webhook', methods=['POST', 'OPTIONS'])
def bot_webhook():
    try:
        payload = request.get_json()
        print("Request received from frontend:", payload)

        if 'action' not in payload:
            raise KeyError("'action' field is missing in the payload.")

        action = payload['action']
        message = payload.get('message', '')
        user_id = payload.get('userId', 'Unknown User')

        if action == "processMessage":
            response = handle_analytics_query(message)
            return jsonify({"reply": response})

        elif action == "getBotDetails":
            bot_details = {
                "_id": "bot",
                "name": "Admin Bot",
                "role": "bot"
            }
            return jsonify(bot_details)

        return jsonify({"error": f"Unsupported action: {action}"}), 400

    except KeyError as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Bot server is up and running 🚀"}), 200

if __name__ == "__main__":
    print("Starting Waitress server...")
    serve(app, host="0.0.0.0", port=5055)
