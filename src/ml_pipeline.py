import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
import joblib
import os

# 1 Carregar o dataset
DATA_PATH = "data/processed/dataset_evasao_escolar.csv"
df = pd.read_csv(DATA_PATH)

# 2 Pré-processamento
X = df[["taxa_evasao", "ideb", "infra_index", "renda_media", "desemprego"]]
y = df["risco_evasao"]

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3 Treinar modelo Gradient Boosting
model = GradientBoostingClassifier(random_state=42)
model.fit(X_train, y_train)

# 4 Avaliação
y_pred = model.predict(X_test)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("==== Relatório de Classificação ====")
print(classification_report(y_test, y_pred))

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")

# 5 Garantir que diretórios existem
os.makedirs("data/models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# 6 Salvar modelo treinado
MODEL_PATH = "data/models/modelo_evasao_escolar.pkl"
joblib.dump(model, MODEL_PATH)
print(f"Modelo salvo em: {MODEL_PATH}")

# 7 Salvar importâncias das features em CSV
feature_importance = pd.Series(model.feature_importances_, index=X.columns)
FEATURES_PATH = "data/processed/feature_importance.csv"
feature_importance.to_csv(FEATURES_PATH)
print(f"Feature importance salva em: {FEATURES_PATH}")
