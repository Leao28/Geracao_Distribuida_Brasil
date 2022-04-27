# import python libraries
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

##--------------------------------------------------------------------------------------------##
print('\nO arquivo python está sendo executado.')
##--------------------------------------------------------------------------------------------##
# Reading file with pandas
df_Base = pd.read_csv('Output/DataFrame_Base.csv', sep = ';', encoding = 'UTF-8')
df_Tarifas = pd.read_csv('Output/DataFrame_Tarifas.csv', sep = ';', encoding = 'UTF-8')
print('\nA base de dados foi importada com sucesso.')

##--df_Unidades_Conectadas_UF-----------------------------------------------------------------##
# Selecting df_Base columns
df_Unidades_Conectadas_UF = [df_Base['UF'], df_Base['Pot_Instalada_kW']]

# Concatenate dataframe list
df_Unidades_Conectadas_UF = pd.concat(df_Unidades_Conectadas_UF, axis = 1)

# Grouping by count and sum of values
df_Unidades_Conectadas_UF = pd.concat([df_Unidades_Conectadas_UF.groupby(['UF']).count(), 
                                   df_Unidades_Conectadas_UF.groupby(['UF']).sum()],
                                   axis = 1).reset_index()

df_Unidades_Conectadas_UF.columns = ['UF', 'Unidades_Conectadas', 'Pot_Instalada_kW']
df_Unidades_Conectadas_UF = df_Unidades_Conectadas_UF.sort_values(by= ['UF'])
df_Unidades_Conectadas_UF.index = range(df_Unidades_Conectadas_UF.shape[0])

##--df_Situacao_Regiao------------------------------------------------------------------------##
# Selecting df_Base columns
df_Unidades_Conectadas_Regiao = [df_Base.query('Data_Conexao < "2021-04-01"')['Regiao'], 
    df_Base.query('Data_Conexao < "2021-04-01"')['Pot_Instalada_kW']]

# Concatenate dataframe list
df_Unidades_Conectadas_Regiao = pd.concat(df_Unidades_Conectadas_Regiao, axis = 1)

# Grouping by count and sum of values
df_Unidades_Conectadas_Regiao = pd.concat([df_Unidades_Conectadas_Regiao.groupby(['Regiao']).count(), 
    df_Unidades_Conectadas_Regiao.groupby(['Regiao']).sum()],
    axis = 1).reset_index()

df_Unidades_Conectadas_Regiao.columns = ['Regiao', 'Unidades_Conectadas', 'Pot_Instalada_kW']
df_Unidades_Conectadas_Regiao = df_Unidades_Conectadas_Regiao.sort_values(by= ['Regiao'])
df_Unidades_Conectadas_Regiao.index = range(df_Unidades_Conectadas_Regiao.shape[0])

# Combining the dataframes
df_Situacao_Regiao = df_Unidades_Conectadas_Regiao.merge(df_Tarifas.\
    query('Data_Referencia == "2021-03-01" and Regiao != "Brasil"'), on=['Regiao'], how = 'outer')

# Deleting, renaming and reordering columns
df_Situacao_Regiao.drop(columns = ['Tarifa_Media_R$'], inplace = True)
df_Situacao_Regiao.columns = ['Regiao', 'UC_GD', 'Pot_Instalada_GD_kW', 'Consumo_Total_MWh', 
    'UC_Total', 'Tarifa_R$', 'Data_Referencia']
df_Situacao_Regiao = df_Situacao_Regiao[['Regiao', 'UC_GD', 'UC_Total', 'Pot_Instalada_GD_kW', 
    'Consumo_Total_MWh', 'Tarifa_R$', 'Data_Referencia']]

##--------------------------------------------------------------------------------------------##
# Exporting DataFrames in .csv
df_Unidades_Conectadas_UF.to_csv('Output/Dataframe_Unidades_Conectadas_UF.csv', sep = ';', encoding = 'UTF-8', index = False)
df_Situacao_Regiao.to_csv('Output/Dataframe_Situacao_Regiao.csv', sep = ';', encoding = 'UTF-8', index = False)
print('\nOs DataFrames foram importados com sucesso.\n')