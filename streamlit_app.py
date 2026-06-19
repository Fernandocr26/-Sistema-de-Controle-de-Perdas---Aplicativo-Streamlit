import sys

try:
    import streamlit as st  # type: ignore[import]
except ModuleNotFoundError as e:
    raise SystemExit("Streamlit is not installed. Run `pip install streamlit` to use this app.") from e

import pandas as pd  # type: ignore
from datetime import datetime
import os

try:
    from pyairtable import Table
except ImportError:
    Table = None

# Nome do arquivo onde os dados serão salvos
DATA_FILE = "perdas.csv"

AIRTABLE_CONFIG = st.secrets.get("airtable", {})

# Configuração da página do Streamlit
st.set_page_config(page_title="Controle de Perdas", page_icon="📉", layout="wide")

st.title("📉 Sistema de Controle de Perdas")
st.markdown("Registre e monitore os prejuízos e quebras do seu negócio.")


def has_airtable() -> bool:
    return bool(AIRTABLE_CONFIG.get("api_key") and AIRTABLE_CONFIG.get("base_id") and AIRTABLE_CONFIG.get("table_name") and Table is not None)


def load_airtable_data() -> pd.DataFrame:
    table = Table(
        AIRTABLE_CONFIG["api_key"],
        AIRTABLE_CONFIG["base_id"],
        AIRTABLE_CONFIG["table_name"],
    )
    records = table.all()
    rows = []
    for record in records:
        fields = record.get("fields", {})
        rows.append(
            {
                "Data": fields.get("Data", ""),
                "Produto": fields.get("Produto", ""),
                "Quantidade": fields.get("Quantidade", 0),
                "Motivo": fields.get("Motivo", ""),
                "Custo Total (R$)": fields.get("Custo Total (R$)", 0.0),
            }
        )
    return pd.DataFrame(rows, columns=["Data", "Produto", "Quantidade", "Motivo", "Custo Total (R$)"])


def save_to_airtable(record: dict) -> None:
    table = Table(
        AIRTABLE_CONFIG["api_key"],
        AIRTABLE_CONFIG["base_id"],
        AIRTABLE_CONFIG["table_name"],
    )
    table.create(record)


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    if has_airtable():
        return load_airtable_data()
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Data", "Produto", "Quantidade", "Motivo", "Custo Total (R$)"])


# Inicializar os dados
df_perdas = carregar_dados()

# Interface dividida em duas colunas (Formulário à esquerda, Relatório à direita)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📋 Registrar Nova Perda")

    with st.form(key="form_perda", clear_on_submit=True):
        produto = st.text_input("Nome do Produto/Insumo")
        quantidade = st.number_input("Quantidade Perdida", min_value=1, step=1)
        custo = st.number_input("Custo Total da Perda (R$)", min_value=0.0, step=0.50, format="%.2f")
        motivo = st.selectbox("Motivo da Perda", [
            "Validade Vencida",
            "Avaria/Dano Físico",
            "Erro de Produção",
            "Roubo/Furto",
            "Outros",
        ])
        data_perda = st.date_input("Data da Ocorrência", datetime.now())

        botao_salvar = st.form_submit_button("Salvar Registro")

    if botao_salvar:
        if produto:
            nova_perda = {
                "Data": data_perda.strftime("%Y-%m-%d"),
                "Produto": produto,
                "Quantidade": quantidade,
                "Motivo": motivo,
                "Custo Total (R$)": custo,
            }

            if has_airtable():
                save_to_airtable(nova_perda)
                df_perdas = pd.concat([df_perdas, pd.DataFrame([nova_perda])], ignore_index=True)
            else:
                df_perdas = pd.concat([df_perdas, pd.DataFrame([nova_perda])], ignore_index=True)
                df_perdas.to_csv(DATA_FILE, index=False)

            st.success(f"Perda de '{produto}' registrada com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Por favor, preencha o nome do produto.")

with col2:
    st.subheader("📊 Histórico e Indicadores")

    if not df_perdas.empty:
        total_prejuizo = df_perdas["Custo Total (R$)"].sum()
        total_itens = df_perdas["Quantidade"].sum()

        m1, m2 = st.columns(2)
        m1.metric("Prejuízo Total", f"R$ {total_prejuizo:,.2f}")
        m2.metric("Total de Itens Perdidos", f"{total_itens} un")

        st.write("---")
        st.write("**Últimos registros:**")
        st.dataframe(df_perdas.sort_index(ascending=False), use_container_width=True)

        st.write("**Prejuízo por Motivo:**")
        grafico_dados = df_perdas.groupby("Motivo")["Custo Total (R$)"].sum()
        st.bar_chart(grafico_dados)
    else:
        st.info("Nenhuma perda registrada ainda. Use o formulário ao lado para começar!")
