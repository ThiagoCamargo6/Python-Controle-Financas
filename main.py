import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import os
import shutil

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Meu Controle Financeiro",
    page_icon="💰",
    layout="wide"
)

# --- NOME DO ARQUIVO DE DADOS E CATEGORIAS ---
NOME_ARQUIVO_DADOS = "meus_dados.csv"

CATEGORIAS_GASTOS = ["Moradia", "Alimentação", "Transporte", "Lazer", "Saúde", "Educação", "Outros"]
CATEGORIAS_RECEITAS = ["Salário", "Freelance", "Investimentos", "Outros"]
TODAS_CATEGORIAS = sorted(list(set(CATEGORIAS_GASTOS + CATEGORIAS_RECEITAS)))

# --- FUNÇÕES AUXILIARES ---
def carregar_dados():
    if os.path.exists(NOME_ARQUIVO_DADOS):
        try:
            df = pd.read_csv(NOME_ARQUIVO_DADOS, encoding='utf-8-sig')  # sem sep, pois separador é vírgula padrão
        except UnicodeDecodeError:
            df = pd.read_csv(NOME_ARQUIVO_DADOS, encoding='latin1')

        colunas_esperadas = ['Data', 'Descrição', 'Valor', 'Categoria']
        if not all(col in df.columns for col in colunas_esperadas):
            st.error("⚠️ O arquivo CSV está com estrutura inválida.")
            return pd.DataFrame(columns=colunas_esperadas)

        df['Data'] = pd.to_datetime(df['Data'], errors='coerce').dt.date
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df = df.dropna(subset=['Data', 'Valor'])
        return df
    else:
        return pd.DataFrame(columns=['Data', 'Descrição', 'Valor', 'Categoria'])

def salvar_dados(df):
    if os.path.exists(NOME_ARQUIVO_DADOS):
        shutil.copy(NOME_ARQUIVO_DADOS, NOME_ARQUIVO_DADOS + ".bak")
    df.to_csv(NOME_ARQUIVO_DADOS, index=False, encoding='utf-8-sig')  # vírgula é o padrão
    st.toast("Dados salvos com sucesso no arquivo!", icon="💾")

# --- INICIALIZAÇÃO DO APP ---
if 'dados' not in st.session_state:
    st.session_state.dados = carregar_dados()

st.title("Meu Controle Financeiro Pessoal 💰")

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
tab_geral, *tabs_meses = st.tabs(["Dashboard Geral", *meses])

# --- ABA GERAL ---
with tab_geral:
    st.header("Visão Geral")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])
    with col_btn1:
        if st.button("Salvar Alterações 💾", use_container_width=True):
            salvar_dados(st.session_state.dados)
            st.balloons()
    with col_btn2:
        st.download_button(
            label="Baixar Dados (CSV) ⬇️",
            data=st.session_state.dados.to_csv(index=False, encoding='utf-8-sig'),
            file_name="meus_dados_exportados.csv",
            mime="text/csv",
            use_container_width=True
)


    df_geral = st.session_state.dados.copy()

    if not df_geral.empty:
        df_geral['Data'] = pd.to_datetime(df_geral['Data'])
        anos_disponiveis = sorted(df_geral['Data'].dt.year.unique(), reverse=True)
        ano_selecionado = st.selectbox("Selecione o Ano para análise:", anos_disponiveis, index=0)
        df_geral = df_geral[df_geral['Data'].dt.year == ano_selecionado]

        st.subheader(f"📊 Resumo Financeiro de {ano_selecionado}")
        total_credito = df_geral[df_geral['Valor'] > 0]['Valor'].sum()
        total_debito = df_geral[df_geral['Valor'] < 0]['Valor'].sum()
        saldo_total = total_credito + total_debito
        
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Total de Receitas", f"R$ {total_credito:,.2f}")
        col2.metric("💸 Total de Gastos", f"R$ {abs(total_debito):,.2f}")
        col3.metric("📿 Saldo Anual", f"R$ {saldo_total:,.2f}")

        gastos_ano = df_geral[df_geral['Valor'] < 0].copy()
        if not gastos_ano.empty:
            col_graf1, col_graf2 = st.columns(2)
            with col_graf1:
                st.markdown("##### Evolução dos Gastos Mensais")
                gastos_ano['Mês'] = gastos_ano['Data'].dt.to_period('M').astype(str)
                gastos_por_mes = gastos_ano.groupby('Mês')['Valor'].sum().abs().reset_index()
                fig_bar = px.bar(gastos_por_mes, x='Mês', y='Valor')
                fig_bar.update_xaxes(type='category')
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_graf2:
                st.markdown("##### Top 5 Categorias de Gasto")
                gastos_por_categoria_anual = gastos_ano.groupby('Categoria')['Valor'].sum().abs().nlargest(5).reset_index()
                fig_pie_anual = px.pie(gastos_por_categoria_anual, names='Categoria', values='Valor')
                st.plotly_chart(fig_pie_anual, use_container_width=True)
        else:
            st.info(f"Nenhum gasto registrado em {ano_selecionado} para gerar os gráficos.")
    else:
        st.info("Ainda não há dados. Adicione transações nas abas mensais.")

# --- ABAS MENSAIS ---
for i, tab_mensal in enumerate(tabs_meses):
    with tab_mensal:
        mes_selecionado = i + 1
        df_mem = st.session_state.dados.copy()
        df_mem['Data'] = pd.to_datetime(df_mem['Data'], errors='coerce')
        dados_mes = df_mem[df_mem['Data'].dt.month == mes_selecionado].dropna(subset=['Data']).copy()

        creditos = dados_mes[dados_mes['Valor'] > 0]['Valor'].sum()
        debitos = dados_mes[dados_mes['Valor'] < 0]['Valor'].sum()
        saldo = creditos + debitos
        delta_percentual = (saldo / creditos * 100) if creditos > 0 else 0
        delta_cor = "normal" if saldo >= 0 else "inverse"

        st.subheader(f"Resumo de {meses[i]}")
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Receitas do Mês", f"R$ {creditos:,.2f}")
        col2.metric("❌ Gastos do Mês", f"R$ {abs(debitos):,.2f}")
        col3.metric("💰 Saldo do Mês", f"R$ {saldo:,.2f}", delta=f"{delta_percentual:.1f}%", delta_color=delta_cor)

        st.divider()

        with st.expander("➕ Adicionar nova transação"):
            with st.form(key=f"form_adicionar_{mes_selecionado}", clear_on_submit=True):
                data = st.date_input("Data", value=datetime.date.today())
                descricao = st.text_input("Descrição", placeholder="Ex: Conta de luz")
                valor = st.number_input("Valor (use negativo para gastos)", step=0.01, format="%.2f")
                categoria = st.selectbox("Categoria", options=TODAS_CATEGORIAS)
                enviar = st.form_submit_button("Adicionar Transação")

                if enviar:
                    if not descricao or valor == 0:
                        st.warning("Por favor, preencha a descrição e um valor diferente de zero.")
                    else:
                        nova_linha = pd.DataFrame([[data, descricao, valor, categoria]],
                                                  columns=["Data", "Descrição", "Valor", "Categoria"])
                        st.session_state.dados = pd.concat([st.session_state.dados, nova_linha], ignore_index=True)
                        st.toast("Transação adicionada!", icon="🎉")
                        st.rerun()

        st.subheader("📄 Transações do Mês")
        if dados_mes.empty:
            st.info("Nenhuma transação neste mês.")
        
        edited_df = st.data_editor(
            dados_mes,
            key=f"editor_{mes_selecionado}",
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY", required=True),
                "Descrição": st.column_config.TextColumn("Descrição", width="large", required=True),
                "Valor": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", required=True),
                "Categoria": st.column_config.SelectboxColumn("Categoria", options=TODAS_CATEGORIAS, required=True)
            },
            height=400
        )

        if not dados_mes.equals(edited_df):
            indices_inalterados = df_mem.index.difference(dados_mes.index)
            df_inalterado = df_mem.loc[indices_inalterados]
            df_atualizado = pd.concat([df_inalterado, edited_df])
            df_atualizado = df_atualizado.sort_values(by="Data").reset_index(drop=True)
            st.session_state.dados = df_atualizado
            st.rerun()
