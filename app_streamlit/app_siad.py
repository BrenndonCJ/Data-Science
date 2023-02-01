import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from pathlib import Path
import os


# Função para gerar graficos
def create_fig1(df1, mode='relative'):
    # Criando as figuras
    fig1 = px.bar(
        df1,
        x='ANO',
        y='CONCLUIDOS',
        barmode=mode,
        color='CURSO',
        category_orders={'ANO':df1['ANO']},
        text='CONCLUIDOS',
        title=''
    )
    fig1.update_layout(plot_bgcolor = 'RGBA(0,0,0,0)')
    fig1.update_xaxes(showgrid=False,showline=True, linewidth=1, linecolor='white')
    fig1.update_yaxes(showgrid=False,showline=True, linewidth=1, linecolor='white')

    template = go.Figure(fig1)
    # template.add_trace(go.Scatter(x=df1['ANO'], y=df1['MEDIA'], name='MEDIA', line=dict(color='RGBA(255,0,0,1)')))

    return template

# Função para gerar graficos
def create_fig2(df1):
    df2 = df1.groupby(['ANO'])['CONCLUIDOS'].sum().reset_index()

    df2['MEDIA ANUAL'] = df1.groupby(['ANO']).agg({'CONCLUIDOS':'mean'}).values

    fig2 = px.bar(
        df2,
        x='ANO',
        y='CONCLUIDOS',
        text='CONCLUIDOS',
        title=''
    )
    fig2.update_layout(plot_bgcolor = 'RGBA(0,0,0,0)')
    fig2.update_xaxes(showgrid=False,showline=True, linewidth=1, linecolor='black')
    fig2.update_yaxes(showgrid=False,showline=True, linewidth=1, linecolor='black')

    template = go.Figure(fig2)
    # template.add_trace(go.Scatter(x=df1['ANO'], y=df1['MEDIA'], name='MEDIA GERAL', line=dict(color='RGBA(255,0,0,1)')))
    template.add_trace(go.Scatter(x=df2['ANO'], y=df2['MEDIA ANUAL'], name='MEDIA ANUAL', line=dict(color='RGBA(0,255,0,1)')))

    return template

# Carregamento dos dados
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(os.path.join(BASE_DIR, 'TabelaEstagios.csv')) # Tabela na msm pasta do arquivo .py

# Limpeza dos dados
df.dropna(subset=['DATA_FIM'], inplace=True)
df['ANO'] = df['DATA_FIM'].map(lambda x: str(x)).map(lambda x: x[:4])
df['ANO'] = df.loc[(df['ANO'] != '0201') & (df['ANO'] != '0216'), 'ANO']

# definindo dataframe de uso
df1 = df.groupby(['ANO', 'CURSO'])['SITUACAO'].count().reset_index().rename(columns={'SITUACAO':'CONCLUIDOS'})
df1['MEDIA'] = df1['CONCLUIDOS'].sum() / len(df1['ANO'].unique())

# ========================================

# Iniciando conteudos da tela
st.set_page_config(
         page_icon="🏛",
         layout="wide",
         initial_sidebar_state="expanded"
)

st.title('Observando conjunto de Dados Estagios - Disciplina \'Sistemas de apoio a decisão\'')

# Definindo colunas da tela para area dos filtros
j1, j2, j3 = st.columns([1,1,2])

# elemento de filtro por ano
filter_ano = j1.multiselect(label="Filtro por ANO", options= df1['ANO'].unique())

# elemento de filtro por curso
filter_curso = j3.multiselect(label="Filtro por Curso", options= df1['CURSO'].unique())

# Definindo colunas da tela para ares dos graficos
listColumns = st.columns(2)

# Definindo Titulos de cada coluna
# Coluna 1
listColumns[0].markdown(f"""
    <h3 style='text-align: center'>
        Quantidade de Estagios concluidos por ano/curso
    </h3>
    """,
    unsafe_allow_html=True
)

# Coluna 3
listColumns[1].markdown(f"""
    <h3 style='text-align: center'>
        Total de Estagios concluidos por ano
    </h3>
    """,
    unsafe_allow_html=True
)

# Definindo guias para multiplos graficos na mesma pagina
guias_graficos_coluna_1 = listColumns[0].tabs(['Grafico 1', 'Grafico 2'])
guias_graficos_coluna_2 = listColumns[1].tabs(['Grafico 1'])

# Verificando se os filtros são vazios, caso sejam, os graficos são gerados com todos os dados
if not (filter_ano):
    filter_ano = df1['ANO'].unique()

if not (filter_curso):
    filter_curso = df1['CURSO'].unique()

# Definindo o DataFrame com aplicação dos filtros
dfaux = df1.loc[(df1['ANO'].map(lambda x: x in filter_ano))].drop(columns=['MEDIA'])
dfaux['MEDIA'] = dfaux['CONCLUIDOS'].sum() / len(dfaux['ANO'].unique())

# Gerando graficos da coluna 1
template = create_fig1(dfaux)
template2 = create_fig1(dfaux, mode='group')

# Definindo o DataFrame com aplicação dos filtros
dfaux = df1.loc[(df1['ANO'].map(lambda x: x in filter_ano)) & (df1['CURSO'].map(lambda x: x in filter_curso))]

# Gerando grafico da coluna 2
fig2 = create_fig2(dfaux)

# plotando os graficos
guias_graficos_coluna_1[0].plotly_chart(template, config=dict(displayModeBar=False), width=1100, height=900, use_container_width=True)
guias_graficos_coluna_1[1].plotly_chart(template2, config=dict(displayModeBar=False), width=1100, height=900, use_container_width=True)
guias_graficos_coluna_2[0].plotly_chart(fig2, config=dict(displayModeBar=False), width=1100, height=900, use_container_width=True)

st.write("Análise e template by: [BrenndonCJ](https://github.com/BrenndonCJ)")