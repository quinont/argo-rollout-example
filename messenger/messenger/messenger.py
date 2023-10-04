from flask import Blueprint, jsonify, request
import os
import random
import time

bp = Blueprint("messenger", __name__)

msg = "Hola desde la v1"

error_threshold = int(os.getenv('ERROR_THRESHOLD', 0))
max_delay_ms = int(os.getenv('MAX_DELAY_MS', 0))

@bp.route("/message", methods = ['GET'])
def get_message():
    delay_time = random.randint(0, max_delay_ms) / 1000
    time.sleep(delay_time)

    generated_number = random.randint(0, 99) 
    if error_threshold > generated_number:
        data = {"msg": "ERROR"}
        return jsonify(data), 500

    data = {"msg": msg}
    return jsonify(data)

@bp.route("/message", methods = ['POST'])
def post_message():
    global msg
    msg_new_json = request.json
    if "new_msg" not in msg_new_json:
        data = {"msg": "data without 'new_msg'"}
        return jsonify(data), 400

    msg = msg_new_json["new_msg"]
    data = {"msg": "OK"}
    return jsonify(data)
