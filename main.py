import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

token = 'abishekabishek'
#verify_token = os.environ.get('VERIFY_TOKEN')


@app.route('/webhook', methods=['POST'])
def webhook():
  body = request.get_json()

  # Check the Incoming webhook message
  print(json.dumps(body, indent=2))

  if body.get("object"):
    if (body.get("entry") and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0]
        and body["entry"][0]["changes"][0].get("value").get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]):

      from_ = body["entry"][0]["changes"][0]["value"]["messages"][0][
        "from"]  # extract the phone number from the webhook payload
      msg_body = body["entry"][0]["changes"][0]["value"]["messages"][0][
        "text"]["body"]  # extract the message text from the webhook payload
      data = {
        "messaging_product": "whatsapp",
        "to": from_,
        "text": {
          "body": msg_body
        }
      }
      headers = {"Content-Type": "application/json"}

      url = "https://graph.facebook.com/v16.0/106424885694792/messages?access_token=EAASr2nql34QBO3ZBJOlay9kAjLmQausx4zn2J4IzKDZCKu71rDU02B2NcH4JpBQiNCPc2NxM7ZCIhOiCMwKbIEJ33qhKoJ6Q48E9RUyqZAZAlezdVGapBT7n8kcxcO9HKyzGwXSxa6YrjpwnUmAC1or3KwUqkDuxNYRFTtNGFJyl68v7utlo92p5vZAVu0esEZCRxZBmenRBiwDk4soXCt7isXw1ZBJoZD"
      requests.post(url, json=data, headers=headers)
    return jsonify(status=200)
  else:
    # Return a '404 Not Found' if event is not from a WhatsApp API
    return jsonify(status=404)


@app.route('/webhook', methods=['GET'])
def verify():
  # Parse params from the webhook verification request
  mode = request.args.get("hub.mode")
  token = request.args.get("hub.verify_token")
  challenge = request.args.get("hub.challenge")

  # Check if a token and mode were sent
  if mode and token:
    # Check the mode and token sent are correct
    if mode == "subscribe":
      # Respond with 200 OK and challenge token from the request
      print("WEBHOOK_VERIFIED")
      return jsonify(challenge), 200
    else:
      # Responds with '403 Forbidden' if verify tokens do not match
      return jsonify(status=403)
  else:
    return jsonify(status=404)

port = int(os.environ.get("PORT", 3000))
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=port)
  print(f"App is running on port {port}")

