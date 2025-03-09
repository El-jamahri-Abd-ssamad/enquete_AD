import pandas as pd
#import numpy as np 


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
    
    
    
    # Sauvegarder le fichier nettoyé
    df.to_csv(output_file, index=False)
    print(f"Fichier nettoyé enregistré sous : {output_file}")

if __name__ == '__main__':
    # Load the dataset
    #df = pd.read_csv('data.csv')
    #print(df.head())
    #Check the data info
    #df.info()
    #Check the missing values 
    #print(df.isnull().sum())
    #Statistical Analysis
    #print(df.describe())
    
    #Verifier que vous etes dans le bon repertoire /enquete_AD> 
    df = pd.read_csv('data.csv')
    nettoyer_csv(df, "data_cleaned.csv")
