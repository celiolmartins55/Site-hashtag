import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

# Passo 1: Criar a tela do sistema e conectar ao Google Sheets
st.write("# Sistema de Vendas")

# Estabelece a conexão com a planilha do Google
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê os dados da planilha
tabela = conn.read(spreadsheet=url_planilha, worksheet="Pagina1", ttl=0)

# Remove linhas 100% vazias que o Google Sheets pode trazer acidentalmente
tabela = tabela.dropna(how="all")

# Passo 2: Criar o formulário de cadastro
st.sidebar.write("## Cadastrar venda")
data = st.sidebar.date_input("Data", max_value="today", format="DD/MM/YYYY")
vendedor = st.sidebar.selectbox("Vendedor", ["Ana", "Bruno", "Carla"])
produto = st.sidebar.selectbox("Produto", ["Notebook", "Celular", "Fone"])
quantidade = st.sidebar.number_input("Quantidade", step=1)
valor = st.sidebar.number_input("Valor")
botao = st.sidebar.button("Cadastrar venda")

# Passo 3: Salvar a venda na base de dados (na Nuvem)
if botao:
    # Cria um DataFrame apenas com a nova venda
    nova_venda = pd.DataFrame([{
        "data": str(data), 
        "vendedor": vendedor, 
        "produto": produto, 
        "quantidade": quantidade, 
        "valor": valor
    }])
    
    # Junta a tabela antiga com a nova venda
    tabela_atualizada = pd.concat([tabela, nova_venda], ignore_index=True)
    
    # Envia os dados atualizados para sobrescrever a planilha do Google (AGORA COM O LINK)
    conn.update(spreadsheet=url_planilha, worksheet="Pagina1", data=tabela_atualizada)
    st.success("Venda cadastrada na nuvem com sucesso!")
    
    # Atualiza a variável 'tabela' localmente para que os gráficos atualizem na mesma hora
    tabela = tabela_atualizada

# Passo 4: Mostrar a base de dados na tela
st.write("## Vendas cadastradas")
st.dataframe(tabela)

# Passo 5: Criar o dashboard com os gráficos
st.write("## Dashboard")
soma = tabela["valor"].sum()
st.metric("Faturamento total", f"R${soma}")

grafico = px.bar(tabela, x="vendedor", y="valor", color="produto", barmode="group")
st.plotly_chart(grafico)

grafico2 = px.pie(tabela, names="produto", values="valor")
st.plotly_chart(grafico2)
