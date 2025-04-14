import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

def load_and_preprocess_data(file_path):
    """
    Charge les données depuis un fichier CSV et effectue le prétraitement initial :
      - Création d'une variable cible artificielle à partir des colonnes d'influence.
      - Retourne le DataFrame complet, les features (X) et la cible (y).
    """
    # Chargement des données
    df = pd.read_csv(file_path, encoding='utf-8', sep=',')
    #print("Aperçu des données :")
    #print(df.head())

    # Définition des colonnes d'influence
    influence_cols = [
        "Influence qualité visuelle sur likes",
        "Influence visages sur likes",
        "Impact commentaires partages sur likes",
        "Influence réactivité auteur sur likes",
        "Influence hashtags sur likes",
        "Influence notifications sur likes",
        "Influence événements spécifiques sur likes",
        "Influence mises à jour sur likes"
    ]

    # Création d'un score global en sommant les influences
    df['influence_score'] = df[influence_cols].sum(axis=1)

    # Définition d'un seuil basé sur la médiane pour créer la cible
    threshold = df['influence_score'].median()
    df['target'] = (df['influence_score'] > threshold).astype(int)

    print("\nDistribution de la variable cible générée :")
    print(df['target'].value_counts())

    # Afficher le type de données des features pour vérification
    X = df.drop(columns=['influence_score', 'target'])
    y = df['target']
    #print("\nTypes de données des features :")
    #print(X.dtypes)

    # Retourner aussi le seuil et le DataFrame complet pour les visualisations ultérieures
    return df, X, y, threshold



def build_pipeline():
    """
    Construit et retourne un pipeline contenant :
      - Imputation des valeurs manquantes.
      - Standardisation des features.
      - Modélisation avec RandomForestClassifier.
    """
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),  # Gère les valeurs manquantes
        ('scaler', StandardScaler()),                 # Standardisation des données
        ('classifier', RandomForestClassifier(random_state=42, n_estimators=100))
    ])
    return pipeline

def evaluate_model(model, X_test, y_test):
    """
    Évalue le modèle sur le jeu de test :
      - Affiche le rapport de classification.
      - Affiche la matrice de confusion.
      - Trace la courbe ROC et calcule l'AUC.
    """
    # Prédictions
    y_pred = model.predict(X_test)
    print("\nRapport de classification sur le jeu de test:")
    print(classification_report(y_test, y_pred))

    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap='Blues')
    plt.title("Matrice de Confusion")
    plt.xlabel("Prédictions")
    plt.ylabel("Valeurs réelles")
    plt.show()


def main():

    file_path = 'data_cleaned.csv'
    
    # 1. Chargement et prétraitement des données
    df, X, y, threshold = load_and_preprocess_data(file_path)

    # Séparation des données en jeu d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Création du pipeline de modélisation
    pipeline = build_pipeline()

    # Validation croisée pour une première estimation de la performance
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
    print("\nScores de validation croisée (accuracy) initiaux :", scores)
    print("Accuracy moyenne de validation croisée initiale: {:.2f}%".format(np.mean(scores) * 100))

    # Entraînement du modèle sur l'ensemble du jeu d'entraînement
    pipeline.fit(X_train, y_train)

    # Évaluation du modèle sur le jeu de test
    evaluate_model(pipeline, X_test, y_test)
    
    # Enregistrement du modèle entraîné dans un fichier
    joblib.dump(pipeline, 'like_model.pkl')
    print("Modèle enregistré dans 'like_model.pkl'.")

if __name__ == "__main__":
    main()
