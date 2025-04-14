# Charger les packages nécessaires
library(randomForest)
library(ggplot2)
library(dplyr)

# 1. Charger les données
data <- read.csv("C:\\Users\\HP\\OneDrive\\Documents\\ESISA\\3eme_annee\\S6\\Analyse Donnée II\\TP\\enquete\\enquete_AD\\data_cleaned.csv", encoding = "UTF-8", sep = ",")

# 2. Créer la variable cible comme dans le script Python
influence_cols <- c(
  "Influence.qualite..visuelle.sur.likes",
  "Influence.visages.sur.likes",
  "Impact.commentaires.partages.sur.likes",
  "Influence.re.activite..auteur.sur.likes",
  "Influence.hashtags.sur.likes",
  "Influence.notifications.sur.likes",
  "Influence.e.ve.nements.spe.cifiques.sur.likes",
  "Influence.mises.a..jour.sur.likes"
)


# Calcul du score et création de la cible
data$influence_score <- rowSums(data[influence_cols])
seuil <- median(data$influence_score)
data$target <- ifelse(data$influence_score > seuil, 1, 0)

# 3. Supprimer les colonnes inutiles
data <- data %>% select(-influence_score)

# 4. Séparer X et y
X <- data %>% select(-target)
y <- as.factor(data$target)

# 5. Créer le modèle Random Forest
set.seed(42)
rf_model <- randomForest(x = X, y = y, importance = TRUE, ntree = 100)

# 6. Extraire l’importance des variables
importance_df <- data.frame(
  Variable = rownames(importance(rf_model)),
  Importance = importance(rf_model)[, "MeanDecreaseGini"]
) %>%
  arrange(desc(Importance))

# 7. Afficher le graphique
ggplot(importance_df, aes(x = reorder(Variable, Importance), y = Importance)) +
  geom_bar(stat = "identity", fill = "#0073C2FF") +
  coord_flip() +
  labs(title = "Importance des variables dans le modèle Random Forest",
       x = "Variables",
       y = "Importance (MeanDecreaseGini)") +
  theme_minimal()


