import pandas as pd
import numpy as np
import streamlit as st
import plotly_express as px

dataframe = pd.read_csv('medicacoes_angicos.csv',index_col=0, sep=',')
dataframe ["Ano"] = dataframe["Ano"].astype("string")

st.set_page_config(
    page_title="Medicamentos Angicos",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

Ano = st.sidebar.multiselect(
    key=1,
    label="Ano",
    options=dataframe["Ano"].unique(),
    default=dataframe["Ano"].unique()
)

dataframe = dataframe.query("Ano == @Ano")

st.header(":bar_chart: Medicamentos Angicos")
st.markdown("""
    ### Medicamentos entregues na rede municipal de Angicos.
            """)
st.markdown("#")

atendimentos = round(dataframe["Nº Usuários Atendidos"].sum(),2)
entregue = round(dataframe["Qtd Dispensada"].sum(),2)
total_medic = len(dataframe["CATMAT"].unique())
valor_total = round(dataframe["Valores"].sum(),2)

st.markdown("""___""")

col1, col2, col3, col4 = st.columns([0.4,0.4,0.4,0.2])
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)

col1.metric("Usuários Atendidos", atendimentos)
col2.metric("Medicamentos Entregues", entregue)
col3.metric("Tipos de Medicações", total_medic)
col4.metric("Valor Total dos Produtos", valor_total)

fig_atendidos = px.bar(
    dataframe, 
    x="Ano", 
    y="Nº Usuários Atendidos",
    color= "Ano", 
    title= "Quantidade de Pacientes Atendidos"
    )

fig_saida = px.bar(
    dataframe, 
    x="Ano", 
    y="Qtd Dispensada",
    color= "Unidade de Medida", 
    title= "Medicamentos Entregues"
    )

fig_valor = px.bar(
    dataframe, 
    x="Valores", 
    y="Ano",
    color= "Ano",
    title= "Valores das Medicações por Ano",
    )

fig_valor_produto = dataframe.groupby("Valores").sum().reset_index()
fig_valor_produto = px.area(
    fig_valor_produto, 
    x="CATMAT", 
    y="Valores",
    title="Valores por Produtos",)
fig_valor_produto.update_xaxes(title = 'Código do Produto')
fig_valor_produto.update_yaxes(title = 'Valores')

col5.plotly_chart(fig_atendidos, use_container_width=True)
col6.plotly_chart(fig_saida, use_container_width=True)
col7.plotly_chart(fig_valor, use_container_width=True)
col8.plotly_chart(fig_valor_produto, use_container_width=True)

st.markdown("""___""")

st.dataframe(dataframe)