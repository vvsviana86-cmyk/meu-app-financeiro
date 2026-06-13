import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuração da página
st.set_page_config(page_title="Meu Orçamento", layout="centered")

st.title("💸 Meu Controlador Financeiro")

# 1. Carregando os dados
arquivo_excel = 'meu_orcamento.xlsx'

# Função para ler os dados (com um truque para não dar erro se o arquivo estiver vazio)
def carregar_dados():
    if os.path.exists(arquivo_excel):
        return pd.read_excel(arquivo_excel)
    else:
        # Cria uma tabela vazia com as colunas certas se o arquivo não existir
        return pd.DataFrame(columns=['Descrição', 'Categoria', 'Tipo', 'Forma_Pagamento', 'Valor (R$)', 'Vencimento', 'Status'])

df_financeiro = carregar_dados()

# 2. Formulário para adicionar novos gastos pelo celular
st.header("📝 Adicionar Novo Gasto")

with st.form("novo_gasto_form"):
    descricao = st.text_input("Descrição (Ex: Uber, Almoço)")
    categoria = st.selectbox("Categoria", ["Moradia", "Alimentação", "Transporte", "Assinaturas", "Cuidados Pessoais", "Diversos", "Graduação"])
    tipo = st.radio("Tipo", ["Fixo", "Variável"])
    forma_pag = st.selectbox("Forma de Pagamento", ["Cartão de Crédito", "PIX", "Boleto", "Débito"])
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    
    # Botão de salvar
    submit_button = st.form_submit_button(label="Salvar Gasto")

    if submit_button:
        # Lógica para salvar a nova linha na planilha
        novo_dado = pd.DataFrame([{
            'Descrição': descricao, 'Categoria': categoria, 'Tipo': tipo, 
            'Forma_Pagamento': forma_pag, 'Valor (R$)': valor, 
            'Vencimento': '-', 'Status': 'Pago'
        }])
        df_financeiro = pd.concat([df_financeiro, novo_dado], ignore_index=True)
        df_financeiro.to_excel(arquivo_excel, index=False)
        st.success(f"Gasto '{descricao}' adicionado com sucesso!")
        st.rerun() # Atualiza a página para mostrar o novo gasto

st.divider()

# 3. Painel de Resumo (O que já tínhamos feito antes)
st.header("📊 Resumo do Mês")

if not df_financeiro.empty:
    meu_salario = 5000.00
    total_gasto = df_financeiro['Valor (R$)'].sum()
    saldo = meu_salario - total_gasto

    # O Streamlit cria "cards" de métricas super bonitos
    col1, col2, col3 = st.columns(3)
    col1.metric("Salário", f"R$ {meu_salario:.2f}")
    col2.metric("Total Gasto", f"R$ {total_gasto:.2f}")
    col3.metric("Saldo Restante", f"R$ {saldo:.2f}")

    # 4. O Gráfico
    st.subheader("Distribuição do Orçamento")
    gastos_categoria = df_financeiro.groupby('Categoria')['Valor (R$)'].sum()
    cores = ['#8FBC8F', '#D2B48C', '#F4A460', '#EEDD82', '#CD853F', '#8B4513']
    
    fig, ax = plt.subplots(figsize=(6, 6))
    gastos_categoria.plot(kind='pie', autopct='%1.1f%%', colors=cores, startangle=90, ax=ax)
    ax.set_ylabel('')
    
    # Exibe o gráfico no app
    st.pyplot(fig)
else:
    st.info("Nenhum gasto registrado ainda.")