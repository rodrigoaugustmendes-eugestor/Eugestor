import streamlit as st
import pandas as pd
from datetime import date

# Configuração da página
st.set_page_config(page_title="Eu Gestor", layout="wide")

# Título e Estilo
st.title("📊 Eu Gestor - Minha Carteira")
st.subheader("Gestão simplificada de clientes")

# Criando dados fictícios para você ver como fica
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame([
        {"Cliente": "Empresa Alfa", "Status": "Ativo", "Valor (R$)": 1500.00, "Último Contato": date(2024, 5, 10), "Prioridade": "Alta"},
        {"Cliente": "João Silva", "Status": "Prospecção", "Valor (R$)": 500.00, "Último Contato": date(2024, 5, 15), "Prioridade": "Média"},
    ])

# --- BARRA LATERAL (CADASTRO) ---
st.sidebar.header("➕ Novo Cliente")
with st.sidebar.form("form_cliente"):
    nome = st.text_input("Nome do Cliente/Empresa")
    status = st.selectbox("Status", ["Prospecção", "Ativo", "Inativo", "Pausado"])
    valor = st.number_input("Valor Mensal (R$)", min_value=0.0, step=100.0)
    data_contato = st.date_input("Data do Último Contato", value=date.today())
    prioridade = st.select_slider("Prioridade", options=["Baixa", "Média", "Alta"])
    
    submetido = st.form_submit_button("Salvar Cliente")
    if submetido:
        novo_dado = {"Cliente": nome, "Status": status, "Valor (R$)": valor, "Último Contato": data_contato, "Prioridade": prioridade}
        st.session_state.dados = pd.concat([st.session_state.dados, pd.DataFrame([novo_dado])], ignore_index=True)
        st.success("Cliente salvo!")

# --- PAINEL PRINCIPAL (DASHBOARD) ---
col1, col2, col3 = st.columns(3)
total_clientes = len(st.session_state.dados)
faturamento_total = st.session_state.dados["Valor (R$)"].sum()

col1.metric("Total de Clientes", total_clientes)
col2.metric("Faturamento Mensal", f"R$ {faturamento_total:,.2f}")
col3.metric("Status Ativo", len(st.session_state.dados[st.session_state.dados["Status"] == "Ativo"]))

st.divider()

# --- TABELA DE VISUALIZAÇÃO ---
st.write("### 🔍 Visualização da Carteira")
st.dataframe(st.session_state.dados, use_container_width=True)

# Botão para baixar os dados (Excel/CSV)
csv = st.session_state.dados.to_csv(index=False).encode('utf-8')
st.download_button("📥 Exportar Carteira para CSV", csv, "carteira_eu_gestor.csv", "text/csv")
