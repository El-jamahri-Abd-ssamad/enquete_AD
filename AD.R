# Packages
if(!require(FactoMineR)) install.packages("FactoMineR")
if(!require(factoextra)) install.packages("factoextra")
library(FactoMineR)
library(factoextra)
library(ggplot2)

# 1. Chargement des données
df <- read.csv("C:/Users/HP/OneDrive/Documents/ESISA/3eme_annee/S6/Analyse Donnée II/TP/enquete/enquete_AD/data_cleaned.csv", sep = ",", na.strings = "")
df[] <- lapply(df, as.factor)

# 2. Calcul de l’ACM (avec variables supplémentaires si besoin)
variables_supplementaires <- c("Qualité.du.contenu", 
                               "Fréquence.et.régularité", 
                               "Interactivité.et.engagement", 
                               "Type.de.contenu.recommandé", 
                               "Public.cible.et.stratégie", 
                               "Suggestions.générales")

res.mca <- MCA(df,
               quali.sup = which(colnames(df) %in% variables_supplementaires),
               graph = FALSE)

# 3. Tableau des valeurs propres
eig <- res.mca$eig
eig
eig[1,3]
eig[3,3]
colnames(eig) <- c("eigenvalue", "variance_%", "cumulative_%")
print(head(eig, 10))   # affiche les 10 premiers axes
# Tu peux aussi exporter ce tableau pour PowerPoint/Excel

# 4. Scree plot (courbe des valeurs propres)
fviz_screeplot(res.mca, 
               addlabels = TRUE, 
               ylim = c(0, max(eig[,2]) + 5)) +
  labs(title = "Scree plot : % de variance par axe",
       x = "Axes", y = "% de variance")

# 5. Plans factoriels multiples
# Plan 1–2
p12 <- fviz_mca_biplot(res.mca, 
                       repel     = TRUE,
                       title     = "Plan factoriel 1–2 (20,7 %)",
                       palette   = "jco",
                       label     = "var")
# Plan 1–3
p13 <- fviz_mca_biplot(res.mca, 
                       axes      = c(1, 3),
                       repel     = TRUE,
                       title     = sprintf("Plan factoriel 1–3 (%.1f %%)", 
                                           eig[1,2] + eig[3,2]),
                       palette   = "jco",
                       label     = "var")
# Plan 2–3
p23 <- fviz_mca_biplot(res.mca, 
                       axes      = c(2, 3),
                       repel     = TRUE,
                       title     = sprintf("Plan factoriel 2–3 (%.1f %%)", 
                                           eig[2,2] + eig[3,2]),
                       palette   = "jco",
                       label     = "var")

# Affiche les trois plans côte à côte
library(gridExtra)
grid.arrange(p12, p13, p23, ncol = 2)

# 6. Contributions des variables actives aux axes
# Top 10 variables pour l’axe 1
fviz_contrib(res.mca, choice = "var", axes = 1, top = 10) +
  labs(title = "Top 10 variables contributives à l’axe 1")
# Top 10 variables pour l’axe 2
fviz_contrib(res.mca, choice = "var", axes = 2, top = 10) +
  labs(title = "Top 10 variables contributives à l’axe 2")

# 7. Contributions des modalités (facultatif)
# Par exemple, modalités les plus contributives à l’axe 1
fviz_contrib(res.mca, choice = "var", axes = 1, top = 15, 
             element = "bar", 
             title = "Top 15 modalités contributives à l’axe 1")

