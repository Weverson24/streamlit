import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


st.set_page_config(layout="wide")
st.title("MÉTRICAS DA SEMANA GARANTIA :dart:")
st.logo("Logo-Dufrio.jpg",size="large")
def formatvalor(x):
    return f'R$ {x:.2f}'

with st.sidebar:
    importar_dados = st.file_uploader("Coloque aqui o seu arquivo das notas: ")
    importante = st.toggle("Mostrar painel")


if importante:
    notas,og = st.tabs(["Notas","Portais"])
    with notas:
        if importar_dados is not None:
            ## Importar os dados para o dash
            df = pd.read_excel(importar_dados)
            dfog = pd.read_excel(importar_dados,sheet_name="og")

            with st.sidebar:
                criado = df["Criado por"].unique().tolist()
                criado.insert(0,"")
                criado_por = st.selectbox("Selecione o colaborador: ", criado)

                tipo = df["Tipo de operação"].unique().tolist()
                tipo.insert(0,"")
                gar = st.selectbox("Selecione o tipo de operação:",tipo)
                df = df[df["Tipo de operação"].str.contains(gar)]

                e_mail = st.number_input("Digite a quantidade de e-mail's:",format="%1f")

            

            if criado_por != "":
                df = df[df["Criado por"] == criado_por ]
                dfog = dfog[dfog["Criado por"] == criado_por]

            ## Transformando od dados
            df["Data de lançamento"] = df["Data de lançamento"].dt.strftime('%d/%m/%Y')
            df["Número"] = df["Número"].astype("str")
            df["Conta"] = df["Conta"].astype("str")

            ## Transformando od dados og
            dfog["Data Inicial"] = dfog["Data Inicial"].dt.strftime('%d/%m/%Y')
            dfog["Conta de cliente"] = dfog["Conta de cliente"].astype("str")
            dfog["Site Venda"] = dfog["Site Venda"].astype("str")

            dfog = dfog.drop(columns=['Data Final', 'Site Atendimento','Coluna1'])

            total_operações_og = dfog["Ordem de garantia"].count()

            ogAberto = dfog[dfog["Status"] == "Ordem em aberto"]
            ogAberto_cont = ogAberto["Status"].count()

            ## Operações
            total_operações = df["Número"].count()
            valor_operações = df["Valor total"].sum()

            st.subheader('Resumo de operações:',divider=True)

            c1,c2,c3,c4,c5 = st.columns(5)


            with c1:
                st.metric(label="Total de operações",value=total_operações)

            with c2:
                st.metric(label="Valor das operações",value=formatvalor(valor_operações))

            with c3:
                st.metric(label="Total de E-mails",value=f'{round(e_mail)}')

            with c4:
                st.metric(label="Total de OG`S",value=f'{round(total_operações_og)}')

            with c5:
                st.metric(label="Total de OG`S em aberto",value=f'{round(ogAberto_cont)}')

            g1,g2,g3 = st.columns([2,3,3])

            ## Partes do graficos.

            with g1:
                operacao_colaborador = df.groupby("Criado por")[["Tipo de operação"]].count().reset_index()
                st.subheader('Total de operações:')

                colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

                fig = go.Figure(data=[go.Pie(labels=operacao_colaborador["Criado por"], values=operacao_colaborador["Tipo de operação"], hole=.3)])
                fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=1)))

                fig
            

            with g2:
                operacao_colaborador = df.groupby("Data de lançamento")[["Tipo de operação"]].count().reset_index()
                st.subheader('Operações diarias:')

                fig = px.bar(operacao_colaborador,
                    x="Data de lançamento",
                    y="Tipo de operação",
                    text="Tipo de operação",
                    color="Data de lançamento",
                    barmode="relative",
                    height=450
                    )
                fig.update_traces(textfont=dict(size=16,color="black"))
                fig
            
            with g3:
                operacao_colaborador = df.groupby("Data de lançamento")[["Valor total"]].sum().reset_index()
                st.subheader('Valores diarias:')
                fig = px.bar(operacao_colaborador,
                    x="Data de lançamento",
                    y="Valor total",
                    text="Valor total",
                    color="Data de lançamento",
                    barmode="relative",
                    height=450
                    )
                fig.update_traces(textfont=dict(size=16,color="black"),textposition="outside",texttemplate="%{text:.3s}")
                fig
            
            t1,t2 = st.columns([2,7])
            with t1:
                st.write('ETRADAS E SAIDAS:')
                operacao_colaborador_dir = df.groupby("Direção")[["Valor total"]].count().reset_index()
                operacao_colaborador_dir

                st.write('OPERADOÇÃO POR COLABORADOR:')
                grupo = df.groupby('Criado por').agg({'Valor total': ['count','sum']})
                grupo

                st.write('OG`S EM ABERTO E FECHADOS')
                og_tela = dfog.groupby('Status')[['Ordem de garantia']].count().reset_index()
                og_tela = og_tela.rename(columns={'Ordem de garantia':'Og`s'})
                og_tela

            with t2:
                st.write('OPERADOÇÃO POR COLABORADOR:')
                operacao_colaborador = df.groupby(["Data de lançamento","Criado por"])[["Valor total"]].sum().reset_index()
                fig = px.line(operacao_colaborador,x="Data de lançamento",y="Valor total",color="Criado por",text="Valor total")
                fig.update_traces(textfont=dict(size=16,color="black"),textposition="top right",texttemplate="%{text:.3s}")
                fig


            st.subheader('Tabela com os dados:',divider=True)


            df
            
else:
    st.subheader("Informações importantes!..")
    texto1 = f'''

        Para que o painel seja carregado de forma eficiente, 
        é necessario que a base ou seja a planilha esteja de acordo
        com as informações a seguir.

        >> Todas as notas fiscais, filtre as opções importantes.
        >> Copia as informações na Base e salva o arquivo e pronto.

    '''

    texto2 = f'''

        Por agora mas não menos importante.

        >> Todas as ordens de garantia, filtre as opções importantes.
        >> Copia as informações na Base e salva o arquivo e pronto.
        >> Renomear a planilha como apresentado abaixo " IMPORTANTE ".

    '''

    texto3 = f'''

        E por fim dito tudo.

        Para iniciar as informações do painel, e só ativar esse botão.
        Importante importe os dados para ver melhor.

    '''

    st.text(texto1)
    st.image("Base.png",caption="Todas as notas fiscais")

    st.text(texto2)
    st.image("ogs.png",caption="Todas as ordens de garantia") 


    st.text(texto3)
    st.image("ativar.png",caption="Iniciar o painel") 

    