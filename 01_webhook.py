from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from utils import *
import os
import ast
from flask import jsonify
app = FlaskAPI(__name__)

@app.route("/edo/", methods=['GET'])
def get_correct_edo():
    """
    List or create notes.
    """
    if request.method == 'GET':
        estado = request.args.get('nombre')
        estado_nombre,clave = correct_edo(estado)
        return jsonify({"nombre":estado_nombre, "cve":clave })

@app.route("/mun/", methods=['GET'])
def get_correct_mun():
    """
    List or create notes.
    """
    if request.method == 'GET':
        mun = request.args.get('nombre')
        estado = request.args.get('estado')
        mun_nombre = correct_mun(estado, mun)
        return jsonify({"nombre": mun_nombre})


@app.route("/corner/", methods=['GET', 'POST'])
def get_location_with_corner_municipio():
     """
     List or create notes.
     """
     if request.method == 'GET':
         street_a = str(request.args.get('street_a'))
         street_b = str(request.args.get('street_b'))
         municipio = str(request.args.get('municipio'))
         location = get_location_with_corner_municipio(municipio,street_a,street_b)
         return jsonify(location)


if __name__ == "__main__":
    #Cambiar ip a 0.0.0.0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0", port= int(os.getenv('WEBHOOK_PORT', 5000)))
