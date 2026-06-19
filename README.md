# 📉 Sistema de Controle de Perdas

Um aplicativo Streamlit para registrar e monitorar prejuízos e quebras do seu negócio.

## 🚀 Funcionalidades

- ✅ Registrar novas perdas com data, produto, quantidade e custo
- ✅ Categorizar perdas por motivo (validade, avaria, erro, roubo, etc.)
- ✅ Visualizar histórico completo de perdas
- ✅ Métricas rápidas (prejuízo total e itens perdidos)
- ✅ Gráfico de perdas por motivo

## 📋 Pré-requisitos

- Python 3.8+
- pip

## Persistência no Streamlit Cloud

No Streamlit Community Cloud, o arquivo `perdas.csv` é armazenado no sistema do container e pode ser perdido em deploys ou quando a aplicação reinicia. Para persistência permanente, você pode usar o Airtable como banco de dados externo.

### Airtable (opcional)

1. Crie uma conta em https://airtable.com
2. Crie uma base e uma tabela com os campos:
   - `Data`
   - `Produto`
   - `Quantidade`
   - `Motivo`
   - `Custo Total (R$)`
3. Configure o Streamlit Secrets com:

```toml
[airtable]
api_key = "SUA_API_KEY"
base_id = "SEU_BASE_ID"
table_name = "NomeDaTabela"
```

Quando o Airtable estiver configurado corretamente, o app salvará os registros lá automaticamente.

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Fernandocr26/-Sistema-de-Controle-de-Perdas---Aplicativo-Streamlit.git
cd controle-perdas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como usar

Execute o aplicativo com:
```bash
streamlit run streamlit_app.py
```

Se preferir, também é possível rodar:
```bash
streamlit run app.py
```

Acesse a aplicação em: `http://localhost:8501`

## 📊 Dados

Os dados são salvos em um arquivo `perdas.csv` na mesma pasta do aplicativo.

## 📝 Licença

Este projeto está disponível sob a licença MIT.

---

**Desenvolvido com ❤️ usando Streamlit**
