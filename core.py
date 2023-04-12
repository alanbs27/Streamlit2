import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Dashboard Vendas',
                   page_icon=':bar_chart:',
                   layout='wide'
)
@st.cache
def puxar_dados():
    df = pd.read_excel(
        io='vendas_supermercado.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    
    return df

df = puxar_dados()
#st.dataframe(df)

#-----------sidebar--------
st.sidebar.header("Filtre aqui:")
cidade = st.sidebar.multiselect(
    "Selecione a cidade:",
    options=df['Cidade'].unique(),
    default=df['Cidade'].unique()
)
tipo_cliente = st.sidebar.multiselect(
    "Selecione o cliente:",
    options=df['Tipo_Cliente'].unique(),
    default=df['Tipo_Cliente'].unique()
)
# genero = st.sidebar.multiselect(
#     "Selecione o genero:",
#     options=df['Genero'].unique(),
#     default=df['Genero'].unique()
# )

df_selection = df.query(
    "Cidade == @cidade & Tipo_Cliente == @tipo_cliente"
)
#st.dataframe(df_selection)
#-----------MAINPAGE-----------

st.title(':bar_chart: Dashboard Vendas')
st.markdown('##')

#  KPI's
total_vendas = int(df_selection['Total'].sum())
media_avaliacao = round(df_selection['Avaliação'].mean(), 1)
avaliacao_estrelas = ":star:" * int(round(media_avaliacao, 0))
media_por_venda = round(df_selection['Total'].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total Vendas')
    st.subheader(f'US $ {total_vendas:,}')

with middle_column:
    st.subheader('Média de avaliação')
    st.subheader(f'{media_avaliacao} {avaliacao_estrelas}')

with right_column:
    st.subheader('Média por vendas')
    st.subheader(f'US $ {media_por_venda}')

st.markdown("---")

# vendas por produto [grafico bar]

vendas_por_produto = (
    df_selection.groupby(by=['Linha_Produto']).sum()[['Total']].sort_values(by='Total')
)
fig_vendas_produto = px.bar(
    vendas_por_produto,
    x='Total',
    y=vendas_por_produto.index,
    #color='red',
    title="<b>Vendas por Linha de Produto</b>"
)


total_vendas_genero = (
    df_selection.groupby(by='Genero').sum()[['Total']]
)

fig_vendas_genero = px.bar(
    total_vendas_genero,
    x=total_vendas_genero.index,
    y='Total',
    title='<b> Total vendas por Genero</b>'
)

#st.plotly_chart(fig_vendas_genero)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_vendas_produto, use_container_width=True)
right_column.plotly_chart(fig_vendas_genero, use_container_width=True)






































