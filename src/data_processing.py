import pandas as pd

arquivos = [
    "../tx_rend_escolas_2021.xlsx",
    "../tx_rend_escolas_2022.xlsx",
    "../tx_rend_escolas_2023.xlsx"
]

dfs = [pd.read_excel(arquivo) for arquivo in arquivos]
df_unido = pd.concat(dfs, ignore_index=True)
df_unido.to_csv("../data/rendimento_escolar_2021_2023.csv", index=False)
print("Planilhas unidas e salvas em data/rendimento_escolar_2021_2023.csv")