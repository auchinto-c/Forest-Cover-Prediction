from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin

from predict_from_model import prediction
from prediction_validation_insertion import pred_validation
from training_model import train_model
from training_validation_insertion import train_validation
import flask_monitoringdashboard as dashboard

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/predict', method=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path) # Object Initialization
            pred_val.prediction_validation() # Calling the prediction_validation function

            pred = prediction(path) # Object Initialization
            path = pred.predictionFromModel() # Predicting for dataset present in database

            return Response(f'Prediction File created at {path}')
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path) # Object Initialization
            pred_val.prediction_validation() # Calling the prediction_validation function

            pred = prediction(path) # Object Initialization
            path = pred.predictionFromModel() # Predicting for dataset present in database

            return Response(f'Prediction File created at {path}')

    except ValueError:
        return Response(f'Error Occured:: {ValueError}')
    except KeyError:
        return Response(f'Error Occured:: {KeyError}')
    except Exception as e:
        return Response(f'Error Occured:: {e}')

@app.route('/train', methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path) # object initialization

            train_valObj.trainValidation() # calling the training validation function

            train_modelObj = train_model() # object initialization
            train_modelObj.trainingModel() # training the model for the files

    except ValueError:
        return Response('Error Occured! %s' % ValueError)

    except KeyError:
        return Response('Error Occured! %s' % KeyError)
    
    except Exception as e:
        return Response('Error Occured! %s' % e)

    return Response('Training Successful!')

port = int(os.getenv('PORT', 5001))

if __name__ == '__main__':
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()