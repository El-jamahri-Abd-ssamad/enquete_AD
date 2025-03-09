import pandas as pd
import numpy as np 


def nettoyer_csv(df, output_file):
    #df = pd.read_csv(input_file)

    # Supprimer les lignes entièrement vides
    df.dropna(how='all', inplace=True)

    # Supprimer les lignes contenant au moins une valeur vide (sauf la dernière colonne)
    df.dropna(subset=df.columns[:-1], how='any', inplace=True)

    # Conversion des colonnes spécifiées
    df[df.columns[0]] = df[df.columns[0]].replace({"Homme": 1, "Femme": 0})
    
    # Colonne 6 : Remplacement des valeurs textuelles par des nombres
    impact_mapping = {
        "Impact très positif": 1,
        "Impact modéré": 2,
        "Peu d’impact": 3,
        "Aucun impact": 4
    }
    df[df.columns[5]] = df[df.columns[5]].replace(impact_mapping)
    
    # Colonne 11 : Remplacement des valeurs textuelles par des nombres
    effet_mapping = {
        "oui, positivement": 1,
        "Oui, négativement": 2,
        "Non,aucun impact": 3
    }
    df[df.columns[10]] = df[df.columns[10]].replace(effet_mapping)
    
    # Sauvegarder le fichier nettoyé
    df.to_csv(output_file, index=False)
    print(f"Fichier nettoyé enregistré sous : {output_file}")

if __name__ == '__main__':
    # Load the dataset
    df = pd.read_csv('C:\\Users\\HP\\OneDrive\\Documents\\ESISA\\3eme_annee\\S6\\Analyse Donnée II\\TP\\enquete\\enquete_AD\\heart.csv')
    print(df.head())
    #Check the data info
    print(df.info())
    #Check the missing values 
    print(df.isnull().sum())
    #Statistical Analysis
    print(df.describe())
    nettoyer_csv(df, "heart_cleaned.csv")
