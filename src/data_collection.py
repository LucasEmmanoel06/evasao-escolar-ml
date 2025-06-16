import os
import requests
import json
from pyspark.sql import SparkSession

# Criar sessão Spark
spark = SparkSession.builder \
    .appName("ColetaDadosEvasaoEscolar") \
    .getOrCreate()

# Criar diretórios
os.makedirs("data/raw", exist_ok=True)

# URLs das APIs
MEC_API_URL = "http://dados.gov.br/api/publico/conjuntos-dados"
IBGE_API_URL = "https://servicodados.ibge.gov.br/api/v1/pesquisas"

def fetch_api_data(url):
    """Faz requisição GET e retorna JSON"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def salvar_json_local(data, filepath):
    """Salva JSON em arquivo local"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Dados salvos em {filepath}")

def json_para_sparkdf(json_data):
    """Converte lista de dicts para Spark DataFrame"""
    if not json_data:
        return None
    rdd = spark.sparkContext.parallelize(json_data)
    return spark.read.json(rdd)

def coleta_mec():
    print("Coletando dados do MEC/INEP...")
    dados_mec = fetch_api_data(MEC_API_URL)

    if dados_mec:
        salvar_json_local(dados_mec, "data/raw/mec_datasets_index.json")

        df_mec = json_para_sparkdf(dados_mec.get("result", []))
        if df_mec:
            df_mec.show(5, truncate=False)
            df_mec.write.mode("overwrite").json("data/raw/mec_datasets_index_spark.json")
            print("MEC: DataFrame salvo em formato Spark JSON.")
    else:
        print("Falha na coleta do MEC.")

def coleta_ibge():
    print("Coletando dados do IBGE...")
    dados_ibge = fetch_api_data(IBGE_API_URL)

    if dados_ibge:
        salvar_json_local(dados_ibge, "data/raw/ibge_pesquisas_index.json")

        df_ibge = json_para_sparkdf(dados_ibge)
        if df_ibge:
            df_ibge.show(5, truncate=False)
            df_ibge.write.mode("overwrite").json("data/raw/ibge_pesquisas_index_spark.json")
            print("IBGE: DataFrame salvo em formato Spark JSON.")
    else:
        print("Falha na coleta do IBGE.")

def main():
    coleta_mec()
    coleta_ibge()
    print("Coleta de dados concluída.")
    spark.stop()

if __name__ == "__main__":
    main()
