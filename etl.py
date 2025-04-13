import pandas as pd
import joblib

def load_new_data(file_path):
    """
    Charge les nouvelles données depuis un fichier CSV.
    Les colonnes doivent correspondre aux features attendues par le modèle.
    """
    new_data = pd.read_csv(file_path, encoding='utf-8', sep=',')
    return new_data

def main():
    # Chargement du modèle enregistré
    model = joblib.load('like_model.pkl')
    
    # Chargement des nouvelles données à prédire (ex. 'new_data.csv')
    new_file_path = 'new_data.csv'
    new_data = load_new_data(new_file_path)
    
    # Réalisation des prédictions
    predictions = model.predict(new_data)
    
    # Conversion des prédictions numériques en étiquettes textuelles ("liké" ou "non liké")
    prediction_labels = ["liké" if pred == 1 else "non liké" for pred in predictions]
    
    print("Prédictions pour les nouvelles données :")
    print(prediction_labels)
    
    # Optionnel : Afficher les probabilités de prédiction si nécessaire
    # probabilities = model.predict_proba(new_data)
    # print("Probabilités de prédiction :")
    # print(probabilities)

if __name__ == '__main__':
    main()
