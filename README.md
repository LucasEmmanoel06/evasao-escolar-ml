# Preditor de Evasão Escolar no Ensino Médio
Sistema preditivo de evasão escolar com análise de dados públicos, PySpark e dashboard interativo.

## 🎯 Objetivo
Projeto desenvolvido para prever quais escolas terão alto risco de evasão escolar no Brasil, usando dados do MEC/INEP e IBGE.  
Tecnologias: **PySpark**, **Dash**, **Machine Learning (Gradient Boosting Classifier)**, implantado em **AWS** com segurança avançada.

## ⚙️ Como executar

### ✅ Pré-requisitos
- Pyhon 3.9+
- JDK 17
- Instale as dependências:

```bash
pip install -r requirements.txt
```
### 🚀 Executando o pipeline

### 1️⃣ Coleta de dados
O script `src/data_collection.py` faz a coleta inicial dos índices de datasets do MEC/INEP e IBGE, e salva os arquivos brutos e em formato Spark JSON.

Antes de executar:

- Certifique-se de ter as variáveis de ambiente configuradas no terminal:

```bash
$env:JAVA_HOME = "<caminho para o seu JDK 17>"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
```
- Para rodar a coleta:
```bash
python src/data_collection.py
```
- Os dados serão salvos em:
```bash
data/raw/mec_datasets_index.json
data/raw/ibge_pesquisas_index.json
data/raw/mec_datasets_index_spark.json
data/raw/ibge_pesquisas_index_spark.json
```
### 2️⃣ Processamento dos dados
(A ser implementado no src/data_processing.py)

```bash
python src/data_processing.py
```

### 3️⃣ Treinamento do modelo
(A ser implementado no src/ml_pipeline.py)

```bash
python src/ml_pipeline.py
```

### 4️⃣ Executando o dashboard
(A ser implementado no src/dashboard.py)

```bash
python src/dashboard.py
```

## 📁 Estrutura do projeto
```bash
evasao-escolar-ml/
├── data/
│   ├── raw/
│   ├── processed/
│   └── models/
├── src/
│   ├── data_collection.py
│   ├── data_processing.py
│   ├── ml_pipeline.py
│   └── dashboard.py
├── notebooks/
│   ├── eda.ipynb
│   └── model_evaluation.ipynb
├── reports/
│   └── relatorio_tecnico.pdf
└── requirements.txt
```
