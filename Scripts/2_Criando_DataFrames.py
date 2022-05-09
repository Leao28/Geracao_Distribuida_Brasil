# Importando Bibliotecas
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

##--------------------------------------------------------------------------------------------##
print('\nO arquivo python está sendo executado.')
##--------------------------------------------------------------------------------------------##
# Carregando dados com pandas
df_Base = pd.read_csv('Output/DataFrame_Base.csv', sep = ';', encoding = 'UTF-8')
df_Tarifas = pd.read_csv('Output/DataFrame_Tarifas.csv', sep = ';', encoding = 'UTF-8')
print('\nA base de dados foi importada com sucesso.')

##--------------------------------------------------------------------------------------------##
## Declarando Funções
##--------------------------------------------------------------------------------------------##

def Total_Mini_Micro(Parametro, Parametro_Opcional_1 = 0, Parametro_Opcional_2 = 0, Filtro = 'index == index'):
    if Parametro_Opcional_1 == 0 and Parametro_Opcional_2 == 0:
        # Listando as colunas de interesse
        df_Mini_Micro = [df_Base.query(Filtro)[Parametro], df_Base.query(Filtro)['Pot_Instalada_kW']]
        df_Mini_Micro = pd.concat(df_Mini_Micro, axis = 1)

        # Agrupando pela contagem da quantidade e soma dos valores de potência
        df_Mini_Micro = pd.concat([df_Mini_Micro.groupby([Parametro]).count(), 
            df_Mini_Micro.groupby([Parametro]).sum()],
            axis = 1).reset_index()

        df_Mini_Micro.columns = [Parametro, 'Unidades_Conectadas', 'Pot_Instalada_kW']
        
    elif Parametro_Opcional_1 != 0 and Parametro_Opcional_2 == 0:
    
        df_Mini_Micro = [df_Base.query(Filtro)[Parametro], df_Base.query(Filtro)[Parametro_Opcional_1], 
            df_Base.query(Filtro)['Pot_Instalada_kW']]
        df_Mini_Micro = pd.concat(df_Mini_Micro, axis = 1)

        # Agrupando pela contagem da quantidade e soma dos valores de potência
        df_Mini_Micro = pd.concat([df_Mini_Micro.groupby([Parametro, Parametro_Opcional_1]).count(), 
            df_Mini_Micro.groupby([Parametro, Parametro_Opcional_1]).sum()],
            axis = 1).reset_index()

        df_Mini_Micro.columns = [Parametro, Parametro_Opcional_1, 'Unidades_Conectadas', 'Pot_Instalada_kW']

    elif Parametro_Opcional_1 != 0 and Parametro_Opcional_2 != 0:
        df_Mini_Micro = [df_Base.query(Filtro)[Parametro], df_Base.query(Filtro)[Parametro_Opcional_1], 
            df_Base.query(Filtro)[Parametro_Opcional_2], df_Base.query(Filtro)['Pot_Instalada_kW']]
        df_Mini_Micro = pd.concat(df_Mini_Micro, axis = 1)

        # Agrupando pela contagem da quantidade e soma dos valores de potência
        df_Mini_Micro = pd.concat([df_Mini_Micro.groupby([Parametro, Parametro_Opcional_1, Parametro_Opcional_2]).count(), 
            df_Mini_Micro.groupby([Parametro, Parametro_Opcional_1, Parametro_Opcional_2]).sum()],
            axis = 1).reset_index()

        df_Mini_Micro.columns = [Parametro, Parametro_Opcional_1, Parametro_Opcional_2, 'Unidades_Conectadas', 'Pot_Instalada_kW']

    # Arredondando a coluna 'Pot_Instalada_kW' para 2 casas decimais
    df_Mini_Micro['Pot_Instalada_kW'] = df_Mini_Micro.Pot_Instalada_kW.apply(lambda x: round(x, 2))
    # Adicionando coluna de potência média por unidade
    df_Mini_Micro['Pot_Media_por_Unidade'] = (df_Mini_Micro.Pot_Instalada_kW / df_Mini_Micro.Unidades_Conectadas).round(2)
    df_Mini_Micro.index = range(df_Mini_Micro.shape[0])
    
    return df_Mini_Micro

##--------------------------------------------------------------------------------------------##
## DataFrame 1: Situação Geral por Região
##--------------------------------------------------------------------------------------------##
df_1 = [df_Base.query('Data_Conexao < "2021-04-01"')['Regiao'], 
    df_Base.query('Data_Conexao < "2021-04-01"')['Pot_Instalada_kW']]
df_1 = pd.concat(df_1, axis = 1)

# Agrupando pela contagem da quantidade e soma dos valores de potência
df_1 = pd.concat([df_1.groupby(['Regiao']).count(), 
    df_1.groupby(['Regiao']).sum()],
    axis = 1).reset_index()

df_1.columns = ['Regiao', 'Unidades_Conectadas', 'Pot_Instalada_kW']
df_1 = df_1.sort_values(by= ['Regiao'])
df_1.index = range(df_1.shape[0])

# Combinando DataFrames
df_1 = df_1.merge(df_Tarifas.\
    query('Data_Referencia == "2021-03-01" and Regiao != "Brasil"'), on=['Regiao'], how = 'outer')

df_1.drop(columns = ['Tarifa_Media_R$'], inplace = True)
df_1.columns = ['Regiao', 'UC_GD', 'Pot_Instalada_GD_kW', 'Consumo_Total_MWh', 
    'UC_Total', 'Tarifa_R$', 'Data_Referencia']
df_1 = df_1[['Regiao', 'UC_GD', 'UC_Total', 'Pot_Instalada_GD_kW', 
    'Consumo_Total_MWh', 'Tarifa_R$', 'Data_Referencia']]

##--------------------------------------------------------------------------------------------##
## DataFrame 2: Total de Unidades Conectadas - Por Concessionária
##--------------------------------------------------------------------------------------------##
df_2 = Total_Mini_Micro(Parametro = 'Concessionaria', Parametro_Opcional_1 = 'Sigla')

##--------------------------------------------------------------------------------------------##
## DataFrame 3: Total de Mini e Microgeradoras Conectadas - Por Concessionária
##--------------------------------------------------------------------------------------------##
df_3 = Total_Mini_Micro(Parametro = 'Concessionaria', Parametro_Opcional_1 = 'Sigla', 
Parametro_Opcional_2 = 'Porte_Geracao')

##--------------------------------------------------------------------------------------------##
## DataFrame 4: Total de Mini e Microgeradoras Conectadas - Por Regiao
##--------------------------------------------------------------------------------------------##
df_4 = Total_Mini_Micro(Parametro = 'Regiao', Parametro_Opcional_1 = 'Porte_Geracao')

##--------------------------------------------------------------------------------------------##
## DataFrame 5: Total de Mini e Microgeradoras Conectadas - Por UF
##--------------------------------------------------------------------------------------------##
df_5 = Total_Mini_Micro(Parametro = 'UF', Parametro_Opcional_1 = 'Porte_Geracao')

##--------------------------------------------------------------------------------------------##
## DataFrame 6: Total de Mini e Microgeradoras Conectadas - Por Tipo_Consumidor
##--------------------------------------------------------------------------------------------##
df_6 = Total_Mini_Micro(Parametro = 'Tipo_Consumidor', Parametro_Opcional_1 = 'Porte_Geracao')

##--------------------------------------------------------------------------------------------##
## DataFrame 7: Total de Mini e Microgeradoras Conectadas - Por Classe_Consumo
##--------------------------------------------------------------------------------------------##
df_7 = Total_Mini_Micro(Parametro = 'Classe_Consumo', Parametro_Opcional_1 = 'Porte_Geracao')

##--------------------------------------------------------------------------------------------##
## DataFrame...
##--------------------------------------------------------------------------------------------##



##--------------------------------------------------------------------------------------------##
# Exporting DataFrames in .csv
df_1.to_csv('Output/Dataframe_Situacao_Regiao.csv', sep = ';', encoding = 'UTF-8', index = False)
df_2.to_csv('Output/Dataframe_Total_Concessionaria.csv', sep = ';', encoding = 'UTF-8', index = False)
df_3.to_csv('Output/Dataframe_MiniMicro_Concessionaria.csv', sep = ';', encoding = 'UTF-8', index = False)
df_4.to_csv('Output/Dataframe_MiniMicro_Regiao.csv', sep = ';', encoding = 'UTF-8', index = False)
df_5.to_csv('Output/Dataframe_MiniMicro_UF.csv', sep = ';', encoding = 'UTF-8', index = False)
df_6.to_csv('Output/Dataframe_MiniMicro_TipoConsumidor.csv', sep = ';', encoding = 'UTF-8', index = False)
df_7.to_csv('Output/Dataframe_MiniMicro_ClasseConsumidor.csv', sep = ';', encoding = 'UTF-8', index = False)
print('\nOs DataFrames foram importados com sucesso.\n')