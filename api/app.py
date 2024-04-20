from flask import Flask, jsonify, request
from functions import getMessageLog
from urllib.parse import unquote
from chatbrain import getResponse
from time import sleep

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':

        data = request.json
        from_ = unquote(data.get('From'))
        to = unquote(data.get('To'))
        message = unquote(data.get('Body'))
        date = unquote(data.get('Date'))
        message_id = unquote(data.get('MessageSID'))

        # Process the data here
        log = getMessageLog(from_, to)
        responses = getResponse(message, log)
        sleep(1)
        return jsonify({'message': responses}), 200
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415

@app.route('/call', methods=['GET', 'POST'])
def newCall():
    if request.method == 'POST':
        data = request.json


        return jsonify({'message': 'Message Handled'}), 200
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415


if __name__ == '__main__':
    app.run(debug=True, port=5000)
