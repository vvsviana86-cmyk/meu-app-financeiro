import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# --- TRUQUE DE DESIGN: FUNDO DE GIRASSOL ---
page_bg_img = '''
<style>
/* Coloca a foto do girassol no fundo de tudo */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1597848212624-a19eb35e2651?q=80&w=1080&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
/* Deixa o topo do aplicativo transparente */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
/* Aplica a sua cor lilás com 88% de transparência para não atrapalhar a leitura */
[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(249, 244, 249, 0.88);
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
# ------------------------------------------
# ------------------------------------------
st.title("🚀 Controle e Previsão Financeira")

arquivo_excel = 'meu_fluxo_caixa.xlsx'

# 1. Nova estrutura inteligente de dados
def carregar_dados():
    if os.path.exists(arquivo_excel):
        return pd.read_excel(arquivo_excel)
    else:
        # Colunas novas para suportar previsão e entradas
        return pd.DataFrame(columns=['Mês_Referência', 'Natureza', 'Categoria', 'Descrição', 'Valor (R$)', 'Status'])

df = carregar_dados()

# 2. Criando Abas para organizar a tela do celular
aba_lancamentos, aba_dashboard = st.tabs(["📝 Novos Lançamentos", "📊 Painel e Previsões"])

with aba_lancamentos:
    st.header("Registrar Movimentação")
    
    with st.form("novo_registro"):
        # Qual mês estamos planejando?
        meses_futuros = ["Junho/2026", "Julho/2026", "Agosto/2026", "Setembro/2026", "Outubro/2026", "Novembro/2026", "Dezembro/2026"]
        mes_ref = st.selectbox("Mês de Referência", meses_futuros)
        
        natureza = st.radio("O que você está registrando?", ["Despesa", "Receita", "Reserva/Investimento"])
        
        # O aplicativo muda as opções dependendo do que você escolheu
        if natureza == "Receita":
            categoria = st.selectbox("Origem", ["Adiantamento (Dia 20)", "Salário (5º dia útil)", "Férias", "13º Salário", "Renda Extra"])
            status = st.selectbox("Status", ["Recebido", "A Receber (Previsão)"])
        
        elif natureza == "Reserva/Investimento":
            categoria = st.selectbox("Destino", ["Reserva de Emergência", "Cofrinho (Objetivos)"])
            status = st.selectbox("Status", ["Guardado", "A Guardar (Previsão)"])
            
        else: # Despesa
            categoria = st.selectbox("Categoria", [
                "Moradia", "Alimentação", "Transporte", "Assinaturas", 
                "Cuidados Pessoais", "Diversos", "Graduação", 
                "Vestimenta", "Tecnologia", "Móveis", "Eletrodomésticos", 
                "Lazer", "Saúde", "Cigarro", "Fatura Cartão de Crédito"
            ])
            status = st.selectbox("Status", ["Pago", "A Pagar (Previsão)"])

        descricao = st.text_input("Descrição detalhada")
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Salvar Registro"):
            novo_dado = pd.DataFrame([{
                'Mês_Referência': mes_ref, 'Natureza': natureza, 
                'Categoria': categoria, 'Descrição': descricao, 
                'Valor (R$)': valor, 'Status': status
            }])
            df = pd.concat([df, novo_dado], ignore_index=True)
            df.to_excel(arquivo_excel, index=False)
            st.success(f"Registro salvo com sucesso para {mes_ref}!")
            st.rerun()

with aba_dashboard:
    st.header("Visão Geral do Mês")
    
    # Filtro para você escolher qual mês quer analisar
    if not df.empty:
        mes_selecionado = st.selectbox("Selecione o mês para análise:", df['Mês_Referência'].unique())
        
        # Filtra os dados apenas para o mês escolhido
        df_mes = df[df['Mês_Referência'] == mes_selecionado]
        
        # Cálculos automáticos do mês
        total_receitas = df_mes[df_mes['Natureza'] == 'Receita']['Valor (R$)'].sum()
        total_despesas = df_mes[df_mes['Natureza'] == 'Despesa']['Valor (R$)'].sum()
        total_reservas = df_mes[df_mes['Natureza'] == 'Reserva/Investimento']['Valor (R$)'].sum()
        
        saldo_livre = total_receitas - total_despesas - total_reservas
        
        # Exibição das métricas
        col1, col2 = st.columns(2)
        col1.metric("Entradas Previstas", f"R$ {total_receitas:.2f}")
        col2.metric("Saídas e Faturas", f"R$ {total_despesas:.2f}")
        
        col3, col4 = st.columns(2)
        col3.metric("Guardado/Investido", f"R$ {total_reservas:.2f}")
        col4.metric("Saldo Livre Estimado", f"R$ {saldo_livre:.2f}")
        
        st.divider()
        
        # Gráfico apenas das despesas para entender os ralos de dinheiro
        st.subheader(f"Composição de Gastos - {mes_selecionado}")
        df_gastos = df_mes[df_mes['Natureza'] == 'Despesa']
        if not df_gastos.empty:
            gastos_cat = df_gastos.groupby('Categoria')['Valor (R$)'].sum()
            fig, ax = plt.subplots(figsize=(5, 5))
            gastos_cat.plot(kind='pie', autopct='%1.1f%%', cmap='Set3', startangle=90, ax=ax)
            ax.set_ylabel('')
            st.pyplot(fig)
        else:
            st.info("Ainda não há despesas lançadas para este mês.")
            
    else:
        st.info("Nenhum dado registrado. Comece a lançar na aba ao lado!")
