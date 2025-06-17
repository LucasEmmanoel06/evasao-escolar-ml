import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import round as spark_round

# Criar sessão Spark
spark = SparkSession.builder.appName("ProcessamentoEvasaoEscolar").getOrCreate()

# Criar diretório processed
os.makedirs("data/processed", exist_ok=True)

# Caminhos dos arquivos
PATH_CENSO = "data/raw/censo_escolar_2021‑2024.csv"
PATH_SOCIO = "data/raw/socioeconomico_2021‑2024.csv"
PATH_OUTPUT = "data/processed/dataset_evasao_final.parquet"

# Leitura dos dados
df_censo = spark.read.csv(PATH_CENSO, header=True, inferSchema=True)
df_socio = spark.read.csv(PATH_SOCIO, header=True, inferSchema=True)

# Mostrar esquema para debug
print("Esquema Censo:")
df_censo.printSchema()
print("Esquema Socio:")
df_socio.printSchema()

# Adicionar coluna code_muni no censo (assumindo primeiros dígitos do code_esc)
df_censo = df_censo.withColumn("code_muni", (df_censo.code_esc / 1000).cast("int"))

# Join nos campos ano, trimestre, code_muni
df_final = df_censo.join(
    df_socio,
    on=["ano", "trimestre", "code_muni"],
    how="left"
)

# Ajustes finais
df_final = df_final.withColumn("taxa_evasao_hist", spark_round(df_final["taxa_evasao_hist"], 2)) \
                   .withColumn("infraestrutura_index", spark_round(df_final["infraestrutura_index"], 2)) \
                   .withColumn("ideb", spark_round(df_final["ideb"], 2)) \
                   .withColumn("delta_ideb", spark_round(df_final["delta_ideb"], 2)) \
                   .withColumn("renda_media", spark_round(df_final["renda_media"], 2)) \
                   .withColumn("desemprego_pct", spark_round(df_final["desemprego_pct"], 2))

# Visualizar amostra
df_final.show(5, truncate=False)

# Salvar no formato parquet (compactado e eficiente)
df_final.write.mode("overwrite").parquet(PATH_OUTPUT)

print(f"Dataset final salvo em {PATH_OUTPUT}")
