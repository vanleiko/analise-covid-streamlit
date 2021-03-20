import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados


def grafico_comparativo(dados_2019, dados_2020, dados_2021, causa="COVID", uf="BRASIL"):

    if uf == "BRASIL":
        total_2020 = dados_2020.groupby("tipo_doenca").sum()
        total_2021 = dados_2021.groupby("tipo_doenca").sum()
    
        if causa == "COVID":
            total_2019 = 0        
            lista = [total_2019, int(total_2020.loc[causa]), int(total_2021.loc[causa])]

        else:
            total_2019 = dados_2019.groupby("tipo_doenca").sum()   
            lista = [int(total_2019.loc[causa]), int(total_2020.loc[causa]), int(total_2021.loc[causa])]

    else:
        total_2020 = dados_2020.groupby(["uf", "tipo_doenca"]).sum()
        total_2021 = dados_2021.groupby(["uf", "tipo_doenca"]).sum()
    
        if causa == "COVID":
            total_2019 = 0        
            lista = [total_2019, int(total_2020.loc[uf, "COVID"]), int(total_2021.loc[uf, "COVID"])]
        else:
            total_2019 = dados_2019.groupby(["uf", "tipo_doenca"]).sum()   
            lista = [int(total_2019.loc[uf, causa]), int(total_2020.loc[uf, causa]), int(total_2021.loc[uf, causa])]
        

    dados = pd.DataFrame({"Total": lista, "Ano": [2019, 2020, 2021]})

    fig, ax = plt.subplots()
    ax = sns.barplot(x="Ano", y="Total", data=dados)
    ax.set_title(f"Total de óbitos por {causa} - {uf}", fontweight="bold", fontsize=18)
    ax.set_xlabel("Ano", fontweight="bold", fontsize=16)
    ax.set_ylabel("Óbitos", fontweight="bold", fontsize=14)
    
    return fig
    

def main():

    obitos_2019 = carrega_dados("..\dados\obitos-2019.csv")
    obitos_2020 = carrega_dados("..\dados\obitos-2020.csv")
    obitos_2021 = carrega_dados("..\dados\obitos-2021.csv")
    tipo_doenca = obitos_2021["tipo_doenca"].unique()
    local = np.append(obitos_2021["uf"].unique(), "BRASIL")
    
    st.title("Total de óbitos no Brasil entre os anos de 2019 e 2021")
    st.markdown("Fonte: Portal da Transparência - Especial COVID-19")
    st.markdown("Atualizado em 20/03/2021, às 02:50h")

    opcao_1 = st.sidebar.selectbox("Selecione a causa do óbito:", tipo_doenca)
    opcao_2 = st.sidebar.selectbox("Selecione o local:", local)
    figura = grafico_comparativo(obitos_2019, obitos_2020, obitos_2021, opcao_1, opcao_2)

    st.pyplot(figura)

        
if __name__ == "__main__":
    main()
