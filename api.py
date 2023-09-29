# imports

from flask import Flask
from flask import request
import os
import pandas as pd
from joblib import load

api = Flask(__name__)
api.config["DEBUG"] = False

# Test pour vérifier le déploiement de l'API
@api.route("/")
def hello_world():
    return "Hello World !"

# Liens vers les sources externes en usage local, ou après déploiement
MODEL = 'small_model_final.joblib'
#DATA_URL = "https://eu.pythonanywhere.com/user/Mapiellifr/files/home/Mapiellifr/OC_P7/small_df_model_final.csv"
#MODEL_URL = "https://github.com/Mapie-llifr/OC_P7/blob/main/" + MODEL
#MODEL = "pipeline_lightGBM_final.joblib"        #local
DATA_URL = "./Docs_projet7/small_df_model_final.csv"  #local
MODEL_URL = MODEL                               # local
SEUIL = 0.20


def load_data(nrows):
    """
    Téléchargement du fichier externe de données

    Parameters
    ----------
    nrows : int : nombre de ligne à télécharger.

    Returns
    -------
    data : DataFrame.

    """
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data = data.drop('TARGET', axis=1)
    return data


def prediction(client):
    """
    Retourne la prédiction du modèle pour un client.

    Parameters
    ----------
    client : int : valeur de 'SK_ID_CURR' pour le client.

    Returns
    -------
    y_pred : float : probabilité de non remboursement pour ce client.
    """
    X_client = df[df['SK_ID_CURR'] == client]
    X_client = X_client.drop('SK_ID_CURR', axis=1)
    y_pred = clf.predict_proba(X_client)[0,1]
    return y_pred


def accord(pred) : 
    """
    definit l'interprétation à faire de la prédiction en fonction du SEUIL. 

    Parameters
    ----------
    pred : float : probabilité de non remboursement.

    Returns
    -------
    pret : int : 1, pret aaccordé ; 5, pret risqué ; 0, pret refusé.

    """
    if pred < SEUIL :
        pret = 1
    elif pred < 0.5 : 
        pret = 5
    else : 
        pret = 0
    return pret


def make_feats(client):
    """
    Retourne un dictionnaire des features les plus importantes localement dans la prédiction. 

    Parameters
    ----------
    client : int : valeur de 'SK_ID_CURR' pour le client.

    Returns
    -------
    feature_importance : dict : clef, nom de la variable ; value, importances dans la prédiction.

    """
    X_client = df[df['SK_ID_CURR'] == client]
    X_client = X_client.drop('SK_ID_CURR', axis=1)
    
    if MODEL == "pipeline_lightGBM_final.joblib":
        feats_pred = clf.predict_proba(X_client, pred_contrib=True)
        importance_serie = pd.Series(data=feats_pred[0,0:-1], 
                                 index=X_client.columns)
        
    elif MODEL == "small_model_final.joblib":
        scaler = clf.named_steps['classifier'].named_steps['scaler']
        values = scaler.transform(X_client)
        feats_pred = clf.named_steps['classifier'].named_steps['lr'].coef_ * values
        importance_serie = pd.Series(data=feats_pred[0], 
                                     index=X_client.columns)
    
    best_feats = importance_serie.loc[importance_serie.abs().sort_values(
                                                ascending=False)[:10].index].round(4)
    feature_importance = best_feats.to_dict()
    return feature_importance

df = load_data(3000)

clf = load(MODEL_URL)

# Fournit sur requete la probabilité de non remboursement et l'interprétation à en faire. 
@api.route("/predict")
def predict():
    if 'id' in request.args:
        id_client = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    pred_val = round(prediction(id_client),4)
    score_metier = accord(pred_val)
    return {'prediction': pred_val, 
            'score': score_metier, 
            'id' : id_client}

# Fournit sur requete la feature importance locale pour les dix meilleurs features. 
@api.route("/feats")
def feat_import():
    clf = load(MODEL_URL)
    if 'id' in request.args:
        id_client = int(request.args['id'])
    else : 
        return "Error: No id field provided. Please specify an id."
    feature_importance = make_feats(id_client)
    return feature_importance

#api.run()       #local

port = int(os.environ.get("PORT", 5000))
api.run(host='0.0.0.0', port=port)

# python api.py
