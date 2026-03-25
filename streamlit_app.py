import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Eu Gestor - Dashboard", layout="wide")

# Estilização CSS para deixar os cartões bonitos
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #1E88E5; }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dados de Exemplo (Enquanto não conectamos o Banco de Dados)
if 'dados' not in st.session_state:
    st.session_state.dados = pd.DataFrame([
        {"Cliente": "Empresa Alfa", "Status": "Ativo", "Valor": 1500.0, "Prioridade": "Alta"},
        {"Cliente": "Fazenda Bandeirante", "Status": "Ativo", "Valor": 500.0, "Prioridade": "Média"},
        {"Cliente": "Consultoria Beta", "Status": "Prospecção", "Valor": 2000.0, "Prioridade": "Baixa"}
    ])

# --- BARRA LATERAL (CADASTRO) ---
with st.sidebar:
    st.header("➕ Novo Cliente")
    with st.form("form_cliente"):
        nome = st.text_input("Nome do Cliente/Empresa")
        status = st.selectbox("Status", ["Prospecção", "Ativo", "Inativo"])
        valor = st.number_input("Valor Mensal (R$)", min_value=0.0)
        prioridade = st.select_slider("Prioridade", options=["Baixa", "Média", "Alta"])
        
        submit = st.form_submit_button("Salvar no Dashboard")
        if submit and nome:
            novo = pd.DataFrame([{"Cliente": nome, "Status": status, "Valor": valor, "Prioridade": prioridade}])
            st.session_state.dados = pd.concat([st.session_state.dados, novo], ignore_index=True)
            st.success("Cliente adicionado!")

# --- PAINEL PRINCIPAL ---
st.title("📊 Eu Gestor - Dashboard de Carteira")
st.markdown("---")

df = st.session_state.dados

# 3. Métricas de Impacto (O que faz você brilhar o olho)
col1, col2, col3, col4 = st.columns(4)
faturamento_total = df[df['Status'] == 'Ativo']['Valor'].sum()
potencial_vendas = df[df['Status'] == 'Prospecção']['Valor'].sum()

col1.metric("💰 Faturamento Ativo", f"R$ {faturamento_total:,.2f}")
col2.metric("🚀 Potencial em Aberto", f"R$ {potencial_vendas:,.2f}")
col3.metric("👥 Total Clientes", len(df))
col4.metric("✅ Clientes Ativos", len(df[df['Status'] == 'Ativo']))

st.markdown("---")

# 4. Gráficos Visuais
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("🎯 Saúde da Carteira")
    fig_pizza = px.pie(df, names='Status', values='Valor', hole=0.5, 
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pizza, use_container_width=True)

with c2:
    st.subheader("📈 Top Clientes (Valor)")
    fig_barras = px.bar(df.sort_values('Valor', ascending=False), 
                        x='Cliente', y='Valor', color='Status',
                        text_auto='.2s', title="Ranking de Faturamento")
    st.plotly_chart(fig_barras, use_container_width=True)

# 5. Tabela Detalhada
st.subheader("🔍 Visualização da Carteira")
st.dataframe(df, use_container_width=True)

# Botão de Reset (Cuidado!)
if st.button("Limpar Dados"):
    st.session_state.dados = pd.DataFrame(columns=["Cliente", "Status", "Valor", "Prioridade"])
    st.rerun()
