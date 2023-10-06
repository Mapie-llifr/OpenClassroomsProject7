# API Pret à Dépenser
Application permettant d'utiliser un modèle de prédiction de remboursement d'emprunt.  

Ce programme a été créé dans le cadre de la formation Data Scientist chez OpenClassrooms.  
Il se base sur les données d'une compétition Kaggle : Home Credit.  

## Fichiers
Programme écrit en language python  
Les données : dans Docs_projet7   
- small_model_final.csv : données de moins de 800 variables sur 3000 clients.   

Autres fichiers :  
- small_model_final.joblib : modèle plus petit que l'original (lightGBM) pour le déploiement, modèle de regression logistique entrainé sur l'ensemble des données fournies par Home Credit, enregistré en format joblib.  
- Procfile : fichier utilisé par Heroku pour mettre en place le server web built-in Flask.  
- .github/workflows/run_test.yml : fichier pour lancement des tests automatiques par GitActions.  


- api.py : fichier principal comprenant l'API utilisant Flask.  
- functions.py : module avec les fonctions pour l'API.  
- variables.py : module avec les variables d'environnement pour l'API. 

## Installation
Installation de Python : https://www.python.org/downloads/  
Installation des dépendences :  
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Requirements
Environnement nécessaire au fonctionnement de l'application :     
- Python, version 3.10  


- cloudpickle==2.2.1
- flask==2.2.2
- imbalanced-learn==0.10.1
- joblib==1.2.0
- lightgbm==3.3.5
- mlflow==2.5.0
- numpy
- pandas==1.5.3
- pickleshare==0.7.5
- regex==2023.8.8
- requests==2.31.0
- scikit-learn==1.2.2
- scipy==1.11.1
- watchdog==3.0.0

## Fonctionnement
L'API reçoit en paramètre de requetes le numéro d'identification du client (valeur de 'SK_ID_CURR').      
Le programme charge les données d'application relatives à ce client.     
L'API utilise le modèle pour prédire la probabilité de non remboursement d'un emprunt.     
Cette probabilité est interprétée, comparée à un SEUIL, en-deçà duquel le pret est accepté.     
Cette probabilté si elle est supérieure au SEUIL, mais inférieure à 0,5, le pret est jugé risqué.     
Si la probabilité est supérieure à 0,5, le pret est refusé.     


Le SEUIL a été determiné en calculant que le risque d'accorder un pret à un client qui ne rembourse pas est dix fois plus important que le manque à gagner à refuser un pret à un client qui aurait remboursé.     


L'API renvoit aussi un dictionnaire contenant les dix features ayant le plus d'importances (en valeur absolue) dans la prédiction réalisée pour ce client.    

## Interface
Une interface est disponible pour cette API : https://github.com/Mapie-llifr/OC_P7     
visible @   https://pret-a-depenser.streamlit.app/

## Déploiement
API sur Heroku :    https://pretadepenser-06a8123a2ba8.herokuapp.com/
