from flask import Blueprint, jsonify, request, render_template, redirect, url_for
import os
import random
import requests

bp = Blueprint("frontend", __name__)

error_threshold = int(os.getenv('ERROR_THRESHOLD', 0))

# Leer de variables de entorno, donde esta el sistema mensaje.
HOST_MESSENGER = os.getenv('HOST_MESSENGER', '192.168.0.226')
PORT_MESSENGER = os.getenv('PORT_MESSENGER', '8081')
PATH_MESSENGER = os.getenv('PATH_MESSENGER', '/message')

URL_MESSENGER = f"http://{HOST_MESSENGER}:{PORT_MESSENGER}{PATH_MESSENGER}"


@bp.route("/", methods=("GET", "POST"))
def index():
    generated_number = random.randint(0, 99) 
    if error_threshold > generated_number:
        return "ERROR", 500
    
    if request.method == "POST":
        body = request.form["body"]
        try:
            headers = {}
            abtest_header = request.headers.get('abtest')
            if abtest_header:
                headers['abtest'] = abtest_header

            new_msg = {"new_msg": body}
            response = requests.post(
                    URL_MESSENGER,
                    headers=headers,
                    json = new_msg)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            msg = f'Error en el cambio de mensaje: {err}'
            return render_template("index.html", msg=msg)
        return redirect(url_for("frontend.index"))

    try:
        headers = {}
        abtest_header = request.headers.get('abtest')
        if abtest_header:
            headers['abtest'] = abtest_header

        response = requests.get(URL_MESSENGER, headers=headers)
        response.raise_for_status()
        msg = response.json()["msg"]
    except requests.exceptions.RequestException as err:
        msg = f'Error en la solicitud: {err}'

    return render_template("index.html", msg=msg)

