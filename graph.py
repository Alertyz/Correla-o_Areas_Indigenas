# Importações
import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar página do Streamlit
st.set_page_config(layout="wide")

# Definição da Classe
class AnaliseDesmatamento:
    def __init__(self):
        self.df_incendios, self.df_indigenas = self.carregar_dados()
        self.filtros_na_barra_lateral()

    def carregar_dados(self):
        """Carrega os conjuntos de dados."""
        df_incendios = pd.read_csv("fires.csv", sep=';')
        df_indigenas = pd.read_csv("dataset_indigenas.csv", sep=';', encoding='latin-1', decimal=',')
        df_incendios['ano'] = df_incendios['date'].str.split('/').str[0].astype(int)
        df_incendios.rename(columns={'class': 'Classe'}, inplace=True)
        return df_incendios, df_indigenas

    def filtros_na_barra_lateral(self):
        """Cria filtros na barra lateral."""
        st.sidebar.header("Filtros")
        anos = ["Todos"] + sorted(self.df_indigenas["ANO"].unique().tolist(), reverse=True)
        self.ano_selecionado = st.sidebar.selectbox("Selecione o ano", anos)
        classes = ["Todos"] + self.df_incendios["Classe"].unique().tolist()
        self.classe_selecionada = st.sidebar.multiselect("Selecione as classes de desmatamento", classes, default=["Todos"])
        estados = ["Todos"] + self.df_incendios["uf"].unique().tolist()
        self.estado_selecionado = st.sidebar.multiselect("Selecione os estados", estados, default=["Todos"])

    def executar(self):
        """Função principal para executar o painel."""
        st.title("Análise de Desmatamento")

        # Filtrando dados com base nas entradas do usuário
        df_incendios_filtrados = self.filtrar_dados_incendios()
        df_indigenas_selecionados = self.filtrar_dados_indigenas()

        # Mostrando gráficos
        col1, col2 = st.columns(2)
        with col1:
            self.grafico_distribuicao_por_classe(df_incendios_filtrados)
        with col2:
            self.grafico_distribuicao_por_estado(df_incendios_filtrados)
        self.grafico_area_por_tribo(df_indigenas_selecionados)
        self.grafico_comparacao_anual(df_incendios_filtrados, df_indigenas_selecionados)

    def filtrar_dados_incendios(self):
        """Filtra o conjunto 'incendios' com base na entrada do usuário."""
        df_filtrado = self.df_incendios.copy()
        if "Todos" not in self.classe_selecionada:
            df_filtrado = df_filtrado[df_filtrado["Classe"].isin(self.classe_selecionada)]
        if "Todos" not in self.estado_selecionado:
            df_filtrado = df_filtrado[df_filtrado["uf"].isin(self.estado_selecionado)]
        if self.ano_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado["ano"] == int(self.ano_selecionado)]
        return df_filtrado

    def filtrar_dados_indigenas(self):
        """Filtra o conjunto 'indigenas' com base na entrada do usuário."""
        if self.ano_selecionado != "Todos":
            return self.df_indigenas[self.df_indigenas["ANO"] == int(self.ano_selecionado)]
        else:
            return self.df_indigenas.copy()

    def grafico_distribuicao_por_classe(self, df):
        """Plota a distribuição dos tipos de desmatamento."""
        if not df.empty:
            fig = px.pie(df, names='Classe', title='Distribuição dos tipos de desmatamento')
            st.plotly_chart(fig)

    def grafico_distribuicao_por_estado(self, df):
        """Plota a distribuição do desmatamento por estados."""
        if not df.empty:
            fig = px.pie(df, names='uf', title='Distribuição dos desmatamentos por estado')
            st.plotly_chart(fig)

    def grafico_area_por_tribo(self, df):
        """Plota a área desmatada por tribo."""
        fig = px.bar(df, x='TRIBO', y='AREA', title=f'Área desmatada por tribo em {self.ano_selecionado}')
        st.plotly_chart(fig)

    def grafico_comparacao_anual(self, df_incendios, df_indigenas):
        """Plota comparação anual entre a quantidade de desmatamento e a área perdida."""
        df_incendios_agrupados = df_incendios.groupby("ano").size().reset_index(name="Quantidade de Desmatamentos")
        df_indigenas_agrupados = df_indigenas.groupby("ANO")["AREA"].sum().reset_index(name="Area Perdida Total")
        df_comparacao = pd.merge(df_incendios_agrupados, df_indigenas_agrupados, left_on="ano", right_on="ANO", how="outer").fillna(0)
        df_comparacao.drop(columns="ANO", inplace=True) 
        fig = px.bar(df_comparacao, x="ano", y=["Quantidade de Desmatamentos", "Area Perdida Total"], barmode="group", title="Comparação Anual")
        st.plotly_chart(fig)

# Execução Principal
if __name__ == '__main__':
    analise = AnaliseDesmatamento()
    analise.executar()
