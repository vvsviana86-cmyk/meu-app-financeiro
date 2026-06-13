import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuração da página
st.set_page_config(page_title="Meu Orçamento", layout="centered")

st.title("💸 Meu Controlador Financeiro")

# 1. Carregando os dados
arquivo_excel = 'meu_orcamento.xlsx'

def carregar_dados():
    if os.path.exists(arquivo_excel):
        return pd.read_excel(arquivo_excel)
    else:
        return pd.DataFrame(columns=['Descrição', 'Categoria', 'Tipo', 'Forma_Pagamento', 'Valor (R$)', 'Vencimento', 'Status'])

df_financeiro = carregar_dados()

# 2. Formulário para adicionar novos gastos pelo celular
st.header("📝 Adicionar Novo Gasto")

with st.form("novo_gasto_form"):
    descricao = st.text_input("Descrição (Ex: Uber, Almoço)")
    
    # LISTA DE CATEGORIAS ATUALIZADA
    categoria = st.selectbox("Categoria", [
        "Moradia", "Alimentação", "Transporte", "Assinaturas", 
        "Cuidados Pessoais", "Diversos", "Graduação", 
        "Vestimenta", "Tecnologia", "Móveis", "Eletrodomésticos", 
        "Lazer", "Saúde", "Cigarro", "Reserva de Emergência"
    ])
    
    tipo = st.radio("Tipo", ["Fixo", "Variável"])
    forma_pag = st.selectbox("Forma de Pagamento", ["Cartão de Crédito", "PIX", "Boleto", "Débito"])
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    
    submit_button = st.form_submit_button(label="Salvar Gasto")

    if submit_button:
        novo_dado = pd.DataFrame([{
            'Descrição': descricao, 'Categoria': categoria, 'Tipo': tipo, 
            'Forma_Pagamento': forma_pag, 'Valor (R$)': valor, 
            'Vencimento': '-', 'Status': 'Pago'
        }])
        df_financeiro = pd.concat([df_financeiro, novo_dado], ignore_index=True)
        df_financeiro.to_excel(arquivo_excel, index=False)
        st.success(f"Gasto '{descricao}' adicionado com sucesso!")
        st.rerun()

st.divider()

# 3. Painel de Resumo (Atualizado sem o Salário Fixo)
st.header("📊 Resumo do Mês")

if not df_financeiro.empty:
    total_gasto = df_financeiro['Valor (R$)'].sum()

    # Mostra apenas o total gasto de forma limpa
    st.metric("Total Gasto no Mês", f"R$ {total_gasto:.2f}")

    # 4. O Gráfico
    st.subheader("Distribuição do Orçamento")
    gastos_categoria = df_financeiro.groupby('Categoria')['Valor (R$)'].sum()
    
    # Nova paleta de cores dinâmica para suportar muitas categorias
    fig, ax = plt.subplots(figsize=(6, 6))
    gastos_categoria.plot(kind='pie', autopct='%1.1f%%', cmap='tab20', startangle=90, ax=ax)
    ax.set_ylabel('')
    
    st.pyplot(fig)
else:
    st.info("Nenhum gasto registrado ainda.")
