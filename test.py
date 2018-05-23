import sys, os, shutil, time, traceback
from sklearn.externals import joblib
from google.cloud import storage
import pandas as pd
from flask import Flask, request, jsonify
from storage import upload_model, delete_model, get_model, load_model


app = Flask(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./service_account.json"

@app.route('/upload', methods=['POST'])
def uploadmodel():
    bucket_name = request.args.get('bucket_name')
    file_name = request.args.get('file_name')
    file_path = request.args.get('file_path')
    return upload_model(bucket_name, file_name, file_path)


@app.route('/getallmodels', methods=['GET'])
def getallmodels():
    bucket_name = request.args.get('bucket_name')
    print (bucket_name)
    return get_model(bucket_name)

@app.route('/load', methods=['GET'])
def getmodel():
    bucket_name = request.args.get('bucket_name')
    file_name = request.args.get('file_name')
    return load_model(bucket_name, file_name)

@app.route('/delete', methods=['POST'])
def deletemodel():
    bucket_name = request.args.get('bucket_name')
    file_name = request.args.get('file_name')
    file_path = request.args.get('file_path')
    return delete_model(bucket_name, file_name, file_path)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
