import pandas as pd
import joblib

def load_new_data(file_path):
    """
    Charge le nouveau fichier de données à partir d'un fichier CSV.
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
    
    print("Prédictions pour les nouvelles données:")
    print(predictions)
    
    # Optionnel : Afficher les probabilités de prédiction
    # probabilities = model.predict_proba(new_data)
    # print("Probabilités de prédiction:")
    # print(probabilities)

if __name__ == '__main__':
    main()
