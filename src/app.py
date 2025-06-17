import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_auth # Importa a biblioteca dash_auth
import os

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'data', 'dados.csv')  # ou apenas 'dados.csv' se estiver no mesmo diretório

# ===========================
# 📥 Ler os dados do CSV
# ===========================
# Certifique-se de que 'dados.csv' está no mesmo diretório ou forneça o caminho completo.
df = pd.read_csv(file_path)


# ===========================
# 🚀 Inicializar o app
# ===========================
app = dash.Dash(__name__)
app.title = 'Dashboard Evasão Escolar'

# ===========================
# 🔐 Configuração de Autenticação
# ===========================
VALID_USERNAME_PASSWORD_PAIRS = {
    'ronilegal': 'tingawinga'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# ===========================
# 🎨 Layout do Dashboard
# ===========================
app.layout = html.Div([
    html.H1('Dashboard de Evasão Escolar', style={'textAlign': 'center', 'margin-bottom': '20px'}),

    html.Div([
        html.Label('Selecione o Município:', style={'font-weight': 'bold', 'margin-right': '10px'}),
        dcc.Dropdown(
            id='municipio-dropdown',
            options=[{'label': m, 'value': m} for m in df['municipio'].unique()],
            value=df['municipio'].unique()[0],  # Primeiro município por padrão
            clearable=False,
            style={'width': '100%'}
        )
    ], style={'width': '80%', 'max-width': '600px', 'margin': '20px auto', 'padding': '15px', 'border-radius': '8px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)', 'background-color': '#f9f9f9', 'display': 'flex', 'align-items': 'center'}),

    dcc.Graph(id='grafico-evasao', style={'margin-top': '30px'}),
    dcc.Graph(id='grafico-ideb', style={'margin-top': '30px'}),
    dcc.Graph(id='grafico-renda-desemprego', style={'margin-top': '30px'}),
    dcc.Graph(id='grafico-risco-evasao', style={'margin-top': '30px'})
], style={'font-family': 'Arial, sans-serif', 'padding': '20px', 'background-color': '#f0f2f5'})

# ===========================
# 🔄 Callbacks dos Gráficos
# ===========================

# 📊 Gráfico de Taxa de Evasão
@app.callback(
    Output('grafico-evasao', 'figure'),
    Input('municipio-dropdown', 'value')
)
def update_grafico_evasao(municipio):
    filtro = df[df['municipio'] == municipio]
    fig = px.line(
        filtro,
        x='ano',
        y='taxa_evasao',
        color='school_id',
        markers=True,
        title=f'Taxa de Evasão - {municipio}',
        labels={'taxa_evasao': 'Taxa de Evasão'}
    )
    fig.update_layout(
        yaxis_tickformat=".0%",
        xaxis=dict(dtick=1, title='Ano'),
        hovermode="x unified",
        template="plotly_white"
    )
    return fig

# 📊 Gráfico de IDEB
@app.callback(
    Output('grafico-ideb', 'figure'),
    Input('municipio-dropdown', 'value')
)
def update_grafico_ideb(municipio):
    filtro = df[df['municipio'] == municipio]
    fig = px.line(
        filtro,
        x='ano',
        y='ideb',
        color='school_id',
        markers=True,
        title=f'IDEB - {municipio}',
        labels={'ideb': 'IDEB'}
    )
    fig.update_layout(
        xaxis=dict(dtick=1, title='Ano'),
        hovermode="x unified",
        template="plotly_white"
    )
    return fig

# 📊 Gráfico de Renda Média vs Desemprego
@app.callback(
    Output('grafico-renda-desemprego', 'figure'),
    Input('municipio-dropdown', 'value')
)
def update_grafico_renda_desemprego(municipio):
    filtro = df[df['municipio'] == municipio]
    fig = px.scatter(
        filtro,
        x='renda_media',
        y='desemprego',
        color='school_id',
        size='infra_index',
        hover_name='ano',
        title=f'Renda Média vs Desemprego - {municipio}',
        labels={'renda_media': 'Renda Média (R$)', 'desemprego': 'Desemprego (%)'},
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title='Renda Média (R$)',
        yaxis_title='Desemprego (%)',
        hovermode="closest"
    )
    return fig

# 📊 Gráfico de Risco de Evasão (barras)
@app.callback(
    Output('grafico-risco-evasao', 'figure'),
    Input('municipio-dropdown', 'value')
)
def update_grafico_risco_evasao(municipio):
    filtro = df[df['municipio'] == municipio]
    # Certifique-se de que 'risco_evasao' e 'ano' existem no seu DataFrame
    if 'risco_evasao' not in filtro.columns or 'ano' not in filtro.columns:
        # Retorna um gráfico vazio ou uma mensagem de erro se a coluna não existir
        return px.bar(title="Dados de Risco de Evasão Indisponíveis")
        
    risco_agg = filtro.groupby(['ano', 'school_id'])['risco_evasao'].mean().reset_index()

    fig = px.bar(
        risco_agg,
        x='ano',
        y='risco_evasao',
        color='school_id',
        barmode='group',
        title=f'Risco de Evasão - {municipio}',
        labels={'risco_evasao': 'Risco de Evasão'},
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Risco de Evasão Médio',
        xaxis=dict(dtick=1)
    )
    return fig


# ===========================
# ▶️ Rodar servidor
# ===========================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))  # Render define PORT automaticamente
    app.run(host='0.0.0.0', port=port, debug=False)
