# Preditor de Evasão Escolar no Ensino Médio
Sistema preditivo de evasão escolar com análise de dados públicos, PySpark e dashboard interativo.

## 🎯 Objetivo
Projeto desenvolvido para prever quais escolas terão alto risco de evasão escolar no Brasil, usando dados do MEC/INEP e IBGE.  
Tecnologias: **PySpark**, **Dash**, **Machine Learning (Gradient Boosting Classifier)**, implantado em **AWS** com segurança avançada.

## ⚙️ Como executar

### 1️⃣ Clone o reposiório:
```bash
git clone http://github.com/LucasEmmanoel06/evasao-escolar-ml.git
cd evasao-escolar-ml
```

### 2️⃣ Instale as dependências:
```bash
pip install -r requirements.txt
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
