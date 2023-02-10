import json
from flask import Flask, Response, abort, jsonify, make_response, request, send_file
from flask_cors import CORS
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
    model = Model
    if (model.setFile(request.files['file']) == 400):
        return ErrorHandler.fileTypeError()
    model.setModelParameters(request.form.get('type'), request.form.get('corrState'),
                             request.form.get('usedDataState'), request.form.get('modelType'))
    print(model.modelParameters.getType())
    print(model.modelParameters.getCorrState())
    print(model.modelParameters.getModelType())
    print(model.modelParameters.getUsedDataState())
    if (model.read() == 400):
        return ErrorHandler.fileReadError(model.getFile())
    print(model.variables.getData().columns.tolist())
    print(model.variables.getData().dtypes['1B_1'])
    print(model.variables.getData().dtypes['HelpIS'])
    return "1"


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
