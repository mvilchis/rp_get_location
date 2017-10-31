from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from utils import *
import os
import ast
from flask import jsonify
app = FlaskAPI(__name__)
KEYS = ['fecha']

@app.route("/<variable_name>", methods=['GET', 'POST'])
def get_nearest_bansefi(variable_name = "fecha"):
    """
    List or create notes.
    """
    if request.method == 'POST':
        request_dic = request.form.to_dict()
        #Obtain values list of rapidpro post
        values_dic = request_dic['values']
        fecha_parsear= values_dic[:values_dic.rfind(variable_name)].split("text")[-1]
        fecha_parsear = fecha_parsear.split(":")[1]
        fecha_parsear = fecha_parsear.split(",")[0]
        fecha_parsear = re.sub(r'"','',fecha_parsear).strip()
        fecha = parse_date(fecha_parsear)
        return jsonify({variable_name:fecha})

if __name__ == "__main__":
    #Cambiar ip a 0.0.0.0
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host="0.0.0.0", port= int(os.getenv('WEBHOOK_PORT', 5000)))
