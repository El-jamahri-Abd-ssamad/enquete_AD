import pandas as pd
import numpy as np 

#Step 2: Load the dataset
# Load the dataset
df = pd.read_csv('C:\\Users\\HP\\OneDrive\\Documents\\ESISA\\3eme_annee\\S6\\Analyse Donnée II\\TP\\enquete-AD\\heart.csv')
print(df.head())

#Check the data info
df.info()

df.isnull().sum()

#Step 2: Statistical Analysis
df.describe()