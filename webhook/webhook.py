from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
    return "Webhook running"

@app.route("/webhook", methods = ["POST"])
def dialogflow_webhook():
    req = request.get_json()

    user_text = (
        req.get("queryResult", {})
           .get("queryText", "")
    )

    return jsonify({
        "fulfillmentText": f"You said: {user_text}"
    })

if __name__ == "__main__":
    app.run(port = 5000, debug = True)