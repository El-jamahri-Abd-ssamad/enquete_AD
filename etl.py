import pandas as pd
#import numpy as np 
import sys 

def nettoyer_csv(df, output_file):
    

    # Supprimer les lignes entièrement vides
    #df.dropna(how='all', inplace=True)

    # Supprimer les lignes contenant au moins une valeur vide (sauf la dernière colonne)
    #df.dropna(subset=df.columns[:-1], how='any', inplace=True)

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
    
    #Ayman : "Colonne 5 et colonne 10 : Remplacement des valeurs textuelles par des nombres"
    # Colonne 5 :
    df['Influence visages sur likes'] = df['Influence visages sur likes'].replace('Oui',1)
    df['Influence visages sur likes'] = df['Influence visages sur likes'].replace('Non',0)
    
    # Colonne 10 :
    df['Influence événements spécifiques sur likes'] = df['Influence événements spécifiques sur likes'].replace('Oui',1)
    df['Influence événements spécifiques sur likes'] = df['Influence événements spécifiques sur likes'].replace('Non',0)
    
    #Colonne 3:
    types_contenu = ["Photo/image", "Vidéo", "Citation / Texte", "Infographie"]
    for contenu in types_contenu:
        df[contenu] = df[df.columns[2]].apply(lambda x: 1 if contenu in str(x) else 0)
    
    # Supprimer la colonne originale "Type de contenu"
    df.drop(columns=[df.columns[2]], inplace=True)

     #Convertion des colonnes oui/non:
    df["Influence hashtags sur likes"] = df["Influence hashtags sur likes"].replace({"Oui": 1, "Non": 0})
    
    
    #Colonne 13:
    # Liste des différentes plages horaires
    plages_horaires = ["6h-9h", "12h-14h", "18h-20h", "Nuit"]

    # Création des colonnes binaires
    for plage in plages_horaires:
        df[plage] = df["Heure idéale pour plus de likes"].apply(lambda x: 1 if plage in str(x) else 0)

    # Suppression de la colonne originale
    df.drop(columns=["Heure idéale pour plus de likes"], inplace=True)

    
    # Sauvegarder le fichier nettoyé
    df.to_csv(output_file, index=False)
    print(f"Fichier nettoyé enregistré sous : {output_file}")

if __name__ == '__main__':
    # Corriger l'encodage de sortie pour la console
    sys.stdout.reconfigure(encoding='utf-8')

     # Charger le dataset avec encodage UTF-8
    df = pd.read_csv('data.csv', encoding="utf-8")

    # Vérifier les premières lignes
    print(df.head())
    

    # Vérifier les informations générales
    print(df.info())

    # Vérifier les valeurs manquantes
    print(df.isnull().sum())

    # Analyse statistique
    print(df.describe())

    # Nettoyer et sauvegarder
    nettoyer_csv(df, "data_cleaned.csv")
