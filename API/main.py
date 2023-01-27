import json
from flask import Flask, Response, request, send_file
from flask_cors import CORS
import pandas as pd
from model import Model, Variables, ExcelGenerator

app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/logit", methods=['POST'])
def Logit():
    file = request.files['file']
    type = request.form.get('type')
    print(type)
    print(file)
    model = Model()
    model.readFile(file)
    model.analyzeModelVariables(type)
    correalation = model.getCorrelation()
    variablesSpec = model.getVariableStats()
    model.getModel()
    model.displayHistory()
    # return {'fileName': file.filename, "result": model.getResult(), "correalation": correalation}
    return {'data': variablesSpec, 'fileName': file.filename, "result": model.getResult(), "correalation": correalation, "correlationRestrictions": model.getCorrelationRestrictions()}

# PAKEISTI PILNAI -> paduo


@app.route('/file/<file>', methods=['GET'])
def File(file):
    print(file)
    return send_file("Results\\"+file+".xlsx")
# model = Model()
# return model.getModel()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
