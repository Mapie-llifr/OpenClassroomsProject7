# imports

from flask import Flask
from flask import request
import os
import pandas as pd
from joblib import load
from app import functions as func
from app import variables as var

api = Flask(__name__)
api.config["DEBUG"] = False

# Test pour vérifier le déploiement de l'API
@api.route("/")
def hello_world():
    return "Hello World !"

# Liens vers les sources externes en usage local, ou après déploiement
MODEL = var.MODEL
DATA_URL = var.DATA_URL
MODEL_URL = var.MODEL_URL  

SEUIL = var.SEUIL


# Fournit sur requete la probabilité de non remboursement et l'interprétation à en faire. 
@api.route("/predict")
def predict():
    if 'id' in request.args:
        id_client = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    pred_val = round(func.prediction(id_client),4)
    score_metier = func.accord(pred_val)
    return {'prediction': pred_val, 
            'score': score_metier, 
            'id' : id_client}

# Fournit sur requete la feature importance locale pour les dix meilleurs features. 
@api.route("/feats")
def feat_import():
    if 'id' in request.args:
        id_client = int(request.args['id'])
    else : 
        return "Error: No id field provided. Please specify an id."
    feature_importance = func.make_feats(id_client)
    return feature_importance

#api.run()       #local

port = int(os.environ.get("PORT", 5000))
api.run(host='0.0.0.0', port=port)

# python api.py
