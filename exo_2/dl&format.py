import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re


# Fonction de nettoyage du texte
def preprocess_text(text):
    text = text.lower()  # Convertir en minuscules
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Supprimer les URLs
    text = re.sub(r'\@\w+|\#', '', text)  # Supprimer les mentions et hashtags
    text = re.sub(r'[^\w\s]', '', text)  # Supprimer la ponctuation
    return text


# Charger les données
file_path = 'Data.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')
print(df.head())

# Garder les colonnes pertinentes
df = df[['Label', 'Top1']]  # Utiliser 'Top1' ou une autre colonne de texte pertinente

# Prétraitement :
# Remplacer les labels pour les rendre binaires (0 et 1)
df['Label'] = df['Label'].replace(4, 1)

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(df['Top1'],
                                                    df['Label'],
                                                    test_size=0.2,
                                                    random_state=42)

# Vectoriser le texte (TF-IDF)
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Modèle de régression logistique
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Sauvegarder le modèle et le vectorizer
joblib.dump(model, "logistic_regression_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
