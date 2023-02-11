from datetime import datetime
import json
from flask import Flask, Response, abort, jsonify, make_response, request, send_file
from flask_cors import CORS
import numpy as np
import pandas as pd
from controllers.errorHandler import ErrorHandler

from controllers.model import Model


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
    print("Model class Initiated ",
          datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    model = Model()
    print("File Set ", datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    if (model.setFile(request.files['file']) == 400):
        return ErrorHandler.fileTypeError()
    print("Model Parameters Set ", datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    model.setModelParameters(request.form.get('type'), request.form.get('corrState'),
                             request.form.get('usedDataState'), request.form.get('modelType'))
    print("Reading Data ", datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    if (model.read() == 400):
        return ErrorHandler.fileReadError(model.file)
    print("Determining Variable Suitability ",
          datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    model.variables.determineVariableSuitability()
    print("Preparing Data ", datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    model.variables.prepareData()
    print("Analyzing Variables ", datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"))
    model.variables.analyzeVariables()

    return model.variables.getVariablesSpecifications()


@app.route("/test", methods=['POST'])
def Test():
    return jsonify(status=400, error="File type is incompatible", description="Ensure File type is correct"), 400

# PAKEISTI PILNAI -> paduo
# formData.append("file", this.selectedFile);
#             formData.append("type", type);
#             formData.append("corrState", correlationState);
#             formData.append("usedDataState", usedDataState);
#             formData.append("modelType", modelType);


@app.route('/file/<file>', methods=['GET'])
def File(file):
    print(file)
    return send_file("Results\\"+file+".xlsx")
# model = Model()
# return model.getModel()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
