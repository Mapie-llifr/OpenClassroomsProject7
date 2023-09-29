# imports
import pandas as pd
from joblib import load
from OpenClassroomsProject7 import variables as var

# Liens vers les sources externes en usage local, ou après déploiement
MODEL = var.MODEL
DATA_URL = var.DATA_URL
MODEL_URL = var.MODEL_URL  

SEUIL = var.SEUIL

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

clf = load(var.MODEL_URL)
