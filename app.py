import sys

try:
    import streamlit as st  # type: ignore[import]
except ModuleNotFoundError as e:
    raise SystemExit("Streamlit is not installed. Run `pip install streamlit` to use this app.") from e

import pandas as pd # type: ignore
from datetime import datetime
import os

# Nome do arquivo onde os dados serão salvos
DATA_FILE = "perdas.csv"

# Função para carregar os dados existentes
def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Data", "Produto", "Quantidade", "Motivo", "Custo Total (R$)"])

# Configuração da página do Streamlit
st.set_page_config(page_title="Controle de Perdas", page_icon="📉", layout="wide")

st.title("📉 Sistema de Controle de Perdas")
st.markdown("Registre e monitore os prejuízos e quebras do seu negócio.")

# Inicializar os dados
df_perdas = carregar_dados()

# Interface dividida em duas colunas (Formulário à esquerda, Relatório à direita)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Registrar Nova Perda")
    
    # Formulário de entrada
    with st.form(key="form_perda", clear_on_submit=True):
        produto = st.text_input("Nome do Produto/Insumo")
        quantidade = st.number_input("Quantidade Perdida", min_value=1, step=1)
        custo = st.number_input("Custo Total da Perda (R$)", min_value=0.0, step=0.50, format="%.2f")
        motivo = st.selectbox("Motivo da Perda", [
            "Validade Vencida", 
            "Avaria/Dano Físico", 
            "Erro de Produção", 
            "Roubo/Furto", 
            "Outros"
        ])
        data_perda = st.date_input("Data da Ocorrência", datetime.now())
        
        botao_salvar = st.form_submit_button("Salvar Registro")

    # Lógica ao clicar no botão
    if botao_salvar:
        if produto:
            # Nova linha de dados
            nova_perda = {
                "Data": data_perda.strftime("%Y-%m-%d"),
                "Produto": produto,
                "Quantidade": quantidade,
                "Motivo": motivo,
                "Custo Total (R$)": custo
            }
            
            # Adiciona ao DataFrame e salva no CSV
            df_perdas = pd.concat([df_perdas, pd.DataFrame([nova_perda])], ignore_index=True)
            df_perdas.to_csv(DATA_FILE, index=False)
            
            st.success(f"Perda de '{produto}' registrada com sucesso!")
            # Recarrega a página para atualizar os gráficos
            st.rerun()
        else:
            st.error("Por favor, preencha o nome do produto.")

with col2:
    st.subheader("📊 Histórico e Indicadores")
    
    if not df_perdas.empty:
        # Métricas Rápidas
        total_prejuizo = df_perdas["Custo Total (R$)"].sum()
        total_itens = df_perdas["Quantidade"].sum()
        
        m1, m2 = st.columns(2)
        m1.metric("Prejuízo Total", f"R$ {total_prejuizo:,.2f}")
        m2.metric("Total de Itens Perdidos", f"{total_itens} un")
        
        st.write("---")
        
        # Tabela de dados recentes
        st.write("**Últimos registros:**")
        st.dataframe(df_perdas.sort_index(ascending=False), use_container_width=True)
        
        # Gráfico simples de perdas por motivo
        st.write("**Prejuízo por Motivo:**")
        grafico_dados = df_perdas.groupby("Motivo")["Custo Total (R$)"].sum()
        st.bar_chart(grafico_dados)
    else:
        st.info("Nenhuma perda registrada ainda. Use o formulário ao lado para começar!")