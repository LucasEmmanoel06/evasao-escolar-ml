import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Exemplo de dados
df = pd.DataFrame({
    "Escola": ["A", "B", "C"],
    "Probabilidade de evasão (%)": [25, 45, 15]
})

# Gráfico
fig = px.bar(df, x="Escola", y="Probabilidade de evasão (%)", title="Risco de evasão por escola")

# Criando o app Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="Dashboard de Evasão Escolar"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
