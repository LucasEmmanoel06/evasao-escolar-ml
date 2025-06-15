import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Carregar rendimento escolar
df_rendimento = pd.read_csv("../data/rendimento_escolar_2021_2023.csv")

# Carregar dados do IBGE e MEC (ajuste o caminho conforme necessário)
df_ibge = pd.read_json("../data/raw/ibge_pesquisas_index.json")
df_mec = pd.read_json("../data/mec_datasets_index.json")

# Exemplo: Selecionar/renomear colunas relevantes
# (ajuste conforme os nomes reais das colunas)
df_rendimento = df_rendimento.rename(columns={
    'taxa_evasao': 'taxa_evasao_historica',
    'ideb': 'ideb_escola'
})

# Supondo que você tenha as colunas de interesse:
# - taxa_evasao_historica
# - ideb_escola
# - infraestrutura_escolar
# - renda_media_municipal
# - taxa_desemprego_local

# Unir os dados (exemplo usando código INEP ou nome da escola)
df = df_rendimento.merge(df_mec, on='codigo_inep', how='left')
df = df.merge(df_ibge, on='municipio', how='left')

# Selecionar features para ML
features = [
    'taxa_evasao_historica',
    'ideb_escola',
    'infraestrutura_escolar',
    'renda_media_municipal',
    'taxa_desemprego_local'
]
df_ml = df[features].dropna()

# Definir variável alvo (exemplo: evasão alta = 1, baixa = 0)
# Ajuste o threshold conforme necessário
df_ml['evasao_alta'] = (df_ml['taxa_evasao_historica'] > 0.2).astype(int)

X = df_ml[features]
y = df_ml['evasao_alta']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestClassifier(random_state=42)
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred))

# Para prever novas escolas:
# nova_escola = pd.DataFrame({...}, index=[0])
# pred = modelo.predict(nova_escola[features])

joblib.dump(modelo, "../models/modelo_evasao.pkl")

# Carregar os arquivos CSV de cada ano
df_2021 = pd.read_csv("tx_rend_escolas_2021.csv")
df_2022 = pd.read_csv("tx_rend_escolas_2022.csv")
df_2023 = pd.read_csv("tx_rend_escolas_2023.csv")

# Unir os dados
df = pd.concat([df_2021, df_2022, df_2023], ignore_index=True)

# Veja as colunas disponíveis
print(df.columns)

# Supondo que exista uma coluna 'taxa_evasao'
# Se não existir, envie o nome das colunas para eu te ajudar a calcular

# Calcular evasão histórica por escola (exemplo: média dos anos)
evasao_hist = df.groupby('codigo_inep')['taxa_evasao'].mean().reset_index()
evasao_hist = evasao_hist.rename(columns={'taxa_evasao': 'taxa_evasao_historica'})

# Junte essa informação ao seu dataset principal
df = df.merge(evasao_hist, on='codigo_inep', how='left')

# Agora você pode usar 'taxa_evasao_historica' como feature no seu pipeline de ML

taxa_evasao = 1 - taxa_aprovacao - taxa_reprovacao