import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from funcoes import collect_data, filtrar_colunas, contar_repeticoes, criar_df_guilherme
from datacleaning import clean_data
from matplotlib.ticker import FuncFormatter

def criar_dataframe_guilherme(df):
    #Previne que o df original seja modificado.
    df_copia = df.copy()
    df_copia = filtrar_colunas(df_copia, 'Atuacao em Territorio Indigena','Qtd Valores Apreendidos','Sigla Unidade Federativa')

    #Remove os estados sem atuação em território indigena.
    estados_ap_ind = df_copia[df_copia['Atuacao em Territorio Indigena'] == 'Sim'].groupby('Sigla Unidade Federativa').size().index
    df_ap_ind = df_copia[df_copia['Sigla Unidade Federativa'].isin(estados_ap_ind)]

    df_agrupado = df_ap_ind.groupby(['Atuacao em Territorio Indigena','Sigla Unidade Federativa'])['Qtd Valores Apreendidos'].mean().reset_index(name="Média")
    df_pivot = df_agrupado.pivot_table(values='Média',  columns=['Atuacao em Territorio Indigena'], index = 'Sigla Unidade Federativa', fill_value=0)
    
    df_pivot.to_csv('dados/df_guilherme.csv')

    return df_pivot

def criar_dataframe_gustavo(df):
    # Cria uma cópia das colunas necessáras do dataframe
    df_copia_gustavo = df.copy()
    df_copia_gustavo = filtrar_colunas(df, "Data da Deflagracao", "Area")

    #Deixando mais curtos os títulos para que a legenda seja mais legível
    df_copia_gustavo.loc[df_copia_gustavo["Area"] == "Crimes Ambientais e Contra o Patrimônio Cultural", "Area"] = "Crimes Ambientais"
    df_copia_gustavo.loc[df_copia_gustavo["Area"] == "Crimes de Ódio e Pornografia Infantil", "Area"] = "Crimes de Ódio e Porn. Infantil"
    
    #Evita que um aviso do pandas apareca criando um novo df
    df_copia_gustavo = df_copia_gustavo.copy()
    df_copia_gustavo["Data de Deflagracao"] = df_copia_gustavo['Data da Deflagracao'].dt.strftime('%m/%Y')

    # Usado para saber as áreas de atuação das operações mais frequêntes
    contagem_area = df_copia_gustavo["Area"].value_counts().index

    # Agrupa por mês e área de atuação as operações
    grouped = df_copia_gustavo.groupby(['Area', 'Data de Deflagracao']).size().unstack(fill_value=0)

    grouped = grouped.loc[contagem_area[:10]]

    grouped.to_csv('dados/df_gustavo.csv')

    return grouped

def criar_dataframe_joao(df):
    df_copia_joao = df.copy()
    df_estados_joao = df_copia_joao.groupby('Sigla Unidade Federativa')['Qtd Valores Apreendidos'].sum().reset_index()
    df_estados_joao = df_estados_joao.rename(columns={'Qtd Valores Apreendidos': 'Total Valores Apreendidos'})
    df_estados_joao = df_estados_joao.sort_values(by='Total Valores Apreendidos', ascending=True)

    df_estados_joao.to_csv('dados/df_joao.csv')

    return df_estados_joao

def criar_dataframe_vinicius(df):
    df_copia_vinicius = df.copy()
    df_estados_vinicius = filtrar_colunas(df_copia_vinicius, "Sigla Unidade Federativa")
    df_estados_vinicius = contar_repeticoes(df_estados_vinicius, "Sigla Unidade Federativa")
    df_estados_vinicius = df_estados_vinicius.rename_axis(index = "ESTADOS")
    
    df_estados_vinicius.to_csv('dados/df_vinicius.csv')

    return df_estados_vinicius

if __name__ == "__main__":
    df = clean_data(collect_data())
    criar_dataframe_guilherme(df)
    criar_dataframe_gustavo(df)
    criar_dataframe_joao(df)
    criar_dataframe_vinicius(df)