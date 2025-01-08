from flask import Flask, request, jsonify
import json
import os
import sqlite3
app = Flask(__name__)

# in memory storage lol
fake_db = {}

@app.route('/set', methods=['POST'])
def set_pair():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    fake_db[key] = value
    with open('recurse.json', 'w') as f:
        json.dump(fake_db, f, indent=4)

    return jsonify({
        'status': 'success!',
        'key': key,
        'value': value
    })

# happy to make this get instead of post, but post more elegant
@app.route('/get', methods=['POST'])
def get_pair():
    data = request.json
    key = data.get('key')
    # value = fake_db.get(key)

    with open('recurse.json') as f:
        data = json.load(f)
        print(data)

    value = data.get(key)

    if value is None:
        return jsonify({
            'status': 'error >.<',
            'message': f'No value found for key {key}'
        }), 404
    else:
        return jsonify({
            'status': 'success!',
            'key': key,
            'value': value,
            'data': data
        })

if __name__ == '__main__':
    app.run(port=4000)