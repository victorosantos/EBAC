import timeit
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configuração do tema do Seaborn
sns.set_theme(
    style='ticks',
    rc={
        'axes.spines.right': False,
        'axes.spines.top': False
    }
)

# Função para carregar os dados com cache
@st.cache_data
def load_data(file_data: str, sep: str) -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=file_data, sep=sep)

# Função para aplicar filtros
def multiselect_filter(data: pd.DataFrame, col: str, selected: list[str]) -> pd.DataFrame:
    if 'all' in selected:
        return data
    return data[data[col].isin(selected)].reset_index(drop=True)

# Função principal
def main():
    st.set_page_config(
        page_title="EBAC | Módulo 19 | Streamlit II | Exercício 1",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar com imagem
    try:
        image = Image.open('img/Bank-Branding.jpg')
        st.sidebar.image(image)
    except FileNotFoundError:
        st.sidebar.write("Imagem não encontrada.")

    # Título principal
    st.markdown('''
    <div style="text-align:center">
        <a href="https://github.com/victorosantos">
            <img src="https://raw.githubusercontent.com/victorosantos/EBAC/main/ebac_logo-data_science.png" alt="ebac_logo-data_science" width=100%>
        </a>
    </div>
    <hr>
    <h3 style="text-align:center;">Módulo 19 | Streamlit II | Exercício 1</h3>
    ''', unsafe_allow_html=True)

    st.write('# Telemarketing analysis')
    st.markdown(body='---')

    start = timeit.default_timer()

    # Carregando os dados
    data_url = "https://raw.githubusercontent.com/victorosantos/EBAC/main/atividade_ebac_m19.csv"
    bank_raw = load_data(file_data=data_url, sep=';')
    bank = bank_raw.copy()

    st.write('Tempo para carregar os dados:', round(timeit.default_timer() - start, 2), 'segundos')

    # Exibindo informações iniciais
    st.write('## Antes dos filtros')
    st.write(bank_raw)
    st.write('Quantidade de linhas:', bank_raw.shape[0])
    st.write('Quantidade de colunas:', bank_raw.shape[1])

    # Formulário na Sidebar
    with st.sidebar.form(key='filter_form'):
        # Filtro de idade
        min_age, max_age = bank['age'].min(), bank['age'].max()
        age_range = st.slider('Idade', min_value=min_age, max_value=max_age, value=(min_age, max_age))

        # Filtro por profissões
        job_options = bank['job'].unique().tolist() + ['all']
        selected_jobs = st.multiselect('Profissões', options=job_options, default=['all'])

        # Filtros adicionais
        filters = {
            'Estado Civil': 'marital',
            'Default': 'default',
            'Financiamento Imobiliário': 'housing',
            'Empréstimo': 'loan',
            'Contato': 'contact',
            'Mês': 'month',
            'Dia da Semana': 'day_of_week',
        }
        selected_filters = {}
        for label, column in filters.items():
            options = bank[column].unique().tolist() + ['all']
            selected_filters[column] = st.multiselect(label, options, default=['all'])

        # Aplicação dos filtros
        bank = bank.query('age >= @age_range[0] and age <= @age_range[1]')
        for column, selected in selected_filters.items():
            bank = multiselect_filter(bank, column, selected)

        submit_button = st.form_submit_button('Aplicar filtros')

    # Exibindo os dados após filtros
    st.write('## Após os filtros')
    st.write(bank)
    st.write('Quantidade de linhas:', bank.shape[0])
    st.write('Quantidade de colunas:', bank.shape[1])

    st.markdown('---')

    # Gráficos
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Gráfico de dados brutos
    bank_raw_target = bank_raw['y'].value_counts(normalize=True).mul(100)
    sns.barplot(x=bank_raw_target.index, y=bank_raw_target.values, ax=axes[0])
    axes[0].set_title('Dados Brutos')
    axes[0].set_ylabel('Porcentagem')
    axes[0].bar_label(axes[0].containers[0])

    # Gráfico de dados filtrados
    bank_target = bank['y'].value_counts(normalize=True).mul(100)
    sns.barplot(x=bank_target.index, y=bank_target.values, ax=axes[1])
    axes[1].set_title('Dados Filtrados')
    axes[1].set_ylabel('Porcentagem')
    axes[1].bar_label(axes[1].containers[0])

    st.write('## Proporção de Aceite')
    st.pyplot(fig)

# Execução
if __name__ == '__main__':
    main()

