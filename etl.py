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

    
    #Colonne 2: Dictionnaire de mapping pour convertir l'âge
    age_mapping = {
        "Moins de 18 ans": 1,
        "18-24 ans": 2,
        "25-34 ans": 3,
        "35-44 ans": 4,
        "45 ans et plus": 5
    }

    # Appliquer la conversion
    df["Âge"] = df["Âge"].map(age_mapping)

    #Colonne 7: # Dictionnaire de mapping pour convertir "Influence réactivité auteur sur likes"
    reactivity_mapping = {
        "Oui": 1,
        "Non": 0
    }

    df["Influence réactivité auteur sur likes"] = df["Influence réactivité auteur sur likes"].map(reactivity_mapping)

    #Colonne 12: Dictionnaire de mapping pour la colonne "Types contenu plus engageants"
    engage_content_mapping = {
        "Contenu suscitant des émotions fortes (joie, surprise, inspiration)": 1,
        "Contenu humoristique ou divertissant": 2,
        "Contenu motivant ou inspirant": 3
    }
    
    # Remplacer les valeurs de la colonne 'Types contenu plus engageants' avec les valeurs numériques
    df["Types contenu plus engageants"] = df["Types contenu plus engageants"].map(engage_content_mapping)

    
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
    
    
    # Vérifier que la colonne 4 existe avant modification
    df["Influence qualité visuelle sur likes"] = df["Influence qualité visuelle sur likes"].replace('Oui',1)
    df["Influence qualité visuelle sur likes"] = df["Influence qualité visuelle sur likes"].replace('Non',0)
        
    # Vérifier que la colonne 9 existe avant modification
    df['Influence notifications sur likes'] = df['Influence notifications sur likes'].replace('Oui, souvent',1)
    df['Influence notifications sur likes'] = df['Influence notifications sur likes'].replace('Parfois',2)
    df['Influence notifications sur likes'] = df['Influence notifications sur likes'].replace('Jamais',3)

        # Nom de la dernière colonne
    last_col_name = "Conseils pour augmenter les likes"

    # Définition des catégories avec des mots-clés associés
    categories = {
        "Qualité du contenu": [
            "visuels de qualité", "qualité du contenu", "images", "vidéos", "haute qualité",
            "attire l’attention", "publication bien présentée", "contenu attractif"
        ],
        "Fréquence et régularité": [
            "poster régulièrement", "régularité", "plusieurs publications", "heures actives",
            "maximiser la visibilité"
        ],
        "Interactivité et engagement": [
            "hashtags pertinents", "interagissez", "audience", "légende engageante",
            "ajouter des réactions", "#"
        ],
        "Type de contenu recommandé": [
            "contenu attractif", "hashtags pertinents", "interagissez", "heures de forte affluence",
            "divertissant", "inspirant", "motivante", "impact positif", "post intéressant",
            "utile", "comique"
        ],
        "Public cible et stratégie": [
            "choisir le public", "public cible", "public intelligent", "like"
        ],
        "Suggestions générales": [
            "nouveauté", "c’est bon", "oui", "non", "rien", "merci", "ok", "flemme"
        ]
    }

    # Vérifier si la dernière colonne contient bien du texte avant traitement
    df[last_col_name] = df[last_col_name].astype(str).fillna("")

    # Créer les nouvelles colonnes avec des 0 et 1
    new_last_columns = {
        cat: df[last_col_name].str.contains('|'.join(mots), case=False, na=False).astype(int)
        for cat, mots in categories.items()
    }

    # Transformer le dictionnaire en DataFrame
    new_last_columns_df = pd.DataFrame(new_last_columns)

    # Remplacer la dernière colonne par les nouvelles colonnes encodées
    df.drop(columns=[last_col_name], inplace=True)
    df = pd.concat([df, new_last_columns_df], axis=1)  # Ajouter les nouvelles colonnes encodées





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
    
    
    # Vérifier les premières lignes du fichier nettoyé
    