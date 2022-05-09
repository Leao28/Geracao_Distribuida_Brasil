# import python libraries
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

##--------------------------------------------------------------------------------------------##
print('\nO arquivo python está sendo executado.')
##--------------------------------------------------------------------------------------------##
# Defining a Function
def criar_dict(index, value):
    dict = df_Base[[index, value]]
    dict.set_index(index, inplace = True)
    dict.drop_duplicates([value], inplace = True)
    dict.dropna(inplace = True)
    dict = dict.to_dict('dict')
    return dict

##--------------------------------------------------------------------------------------------##
# Reading file with pandas
df_Base = pd.read_csv('Input\Dados_Abril_2022.csv', sep = ';', encoding = 'UTF-16')
df_Tarifas = pd.read_csv('Input\Consumo_Tarifa_Por_Regiao.csv', sep = ';', encoding = 'UTF-8')
print('\nA base de dados foi importada com sucesso.')

##--df_Base-----------------------------------------------------------------------------------##
# Removing unnecessary columns
df_Base.drop(columns = ['DatGeracaoConjuntoDados', 'AnmPeriodoReferencia', 'NumCNPJDistribuidora',
    'CodCEP', 'NumCPFCNPJ', 'NomeTitularEmpreendimento', 'SigModalidadeEmpreendimento', 'codRegiao'], inplace = True)

# Reordering columns
df_Base = df_Base[['NomAgente', 'SigAgente', 'CodEmpreendimento', 'SigTipoConsumidor',
'DscClasseConsumo', 'DscSubGrupoTarifario', 'NomMunicipio', 'SigUF', 'NomRegiao', 'SigTipoGeracao', 
'DscFonteGeracao', 'DscPorte', 'MdaPotenciaInstaladaKW', 'DscModalidadeHabilitado', 'QtdUCRecebeCredito', 
'NomSubEstacao', 'DthAtualizaCadastralEmpreend', 'NumCoordNEmpreendimento', 'NumCoordEEmpreendimento', 
'NumCoordESub', 'NumCoordNSub', 'CodClasseConsumo', 'CodSubGrupoTarifario', 'codUFibge', 'CodMunicipioIbge']]

# Renaming Columns
df_Base.columns = ['Concessionaria', 'Sigla', 'Codigo_GD',  'Tipo_Consumidor', 
'Classe_Consumo', 'Grupo_Tarifario', 'Municipio', 'UF', 'Regiao', 'Tipo_Geracao', 
'Fonte_Geracao', 'Porte_Geracao', 'Pot_Instalada_kW', 'Modalidade', 'Unidades_Recebem_Creditos', 
'SubEstacao', 'Data_Conexao', 'Latitude_GD', 'Longitude_GD', 'Latitude_Sub', 'Longitude_Sub',
'ID_Classe', 'ID_Grupo', 'ID_UF', 'ID_Municipio']

# Replacing 'NaN' values in each column
df_Base.fillna({'Concessionaria': 'Não Informado', 'Sigla': 'Não Informado',
    'Tipo_Consumidor': 'Não Informado', 'Municipio': 'Não Informado', 
    'SubEstacao': 'Não Informado'}, inplace = True)

# Substituting 'NaN' values in 'ID_UF' column
dict_UF = criar_dict('UF', 'ID_UF')
for i in range(len(df_Base)):
    df_Base.ID_UF[i] = df_Base.UF[i]
df_Base.fillna({'UF': 'N/I', 'ID_UF': 0.0, 'ID_Municipio': 0.0}, inplace = True)
df_Base.replace({'ID_UF': dict_UF['ID_UF']}, inplace = True)

# Column 'Pot_Instalada_kW' from string to float
df_Base['Pot_Instalada_kW'] = df_Base['Pot_Instalada_kW'].str.replace(',' , '.')
df_Base['Pot_Instalada_kW'] = pd.to_numeric(df_Base['Pot_Instalada_kW'], downcast="float")

# Column 'Data_Conexao' from string to datetime
df_Base['Data_Conexao'] = pd.to_datetime(df_Base['Data_Conexao'], format='%Y/%m/%d')

# Columns from float to int
df_Base = df_Base.astype({'Unidades_Recebem_Creditos': 'int16', 'ID_UF': 'int16', 
    'ID_Classe': 'int16', 'ID_Grupo': 'int16', 'ID_Municipio': 'int32'})

# Replacing column values with a dictionary
df_Base['Modalidade'] = df_Base['Modalidade'].map({
    'Com Microgeracao ou Minigeracao distribuida': 'Geração na própria UC',
    'Caracterizada como Autoconsumo remoto': 'Autoconsumo remoto',
    'Caracterizada como Geracao compartilhada': 'Geracao compartilhada',
    'Integrante de empreendimento de Multiplas UC': 'Integra Multiplas UC'
    }, na_action = None)

df_Base['Porte_Geracao'] = df_Base['Porte_Geracao'].map({
    'Microgeracao': 'Micro Geração',
    'Minigeracao': 'Mini Geração'
    }, na_action = None)

df_Base['Tipo_Consumidor'] = df_Base['Tipo_Consumidor'].map({
    'PF': 'Pessoa Física',
    'PJ': 'Pessoa Jurídica'
    }, na_action = None)

# Sorting dataframe data
df_Base = df_Base.sort_values(by= ['Sigla', 'UF', 'Data_Conexao'])
df_Base.index = range(df_Base.shape[0])

##--df_Tarifas--------------------------------------------------------------------------------##
# Renaming Columns
df_Tarifas.columns = ['Regiao', 'Consumo_MWh', 'Receita_R$',  'Receita_Tributada_R$', 
'Total_UC', 'Tarifa_Media_R$', 'Tarifa_Tributada_R$', 'Mes_Ano', 'Ano']

# Changing column types to float
for i in df_Tarifas:
    if df_Tarifas[i].dtypes == 'object' and i != 'Regiao':
        df_Tarifas[i] = df_Tarifas[i].str.replace(',' , '.')
        df_Tarifas[i] = pd.to_numeric(df_Tarifas[i], downcast="float")

# Creating a column for the reference date
df_Tarifas['Data_Referencia'] = ''
for i in range(len(df_Tarifas)):
    df_Tarifas['Data_Referencia'][i] = df_Tarifas['Ano'].astype(str)[i] + '-' + df_Tarifas['Mes_Ano'].astype(str)[i][4:]
df_Tarifas['Data_Referencia'] = pd.to_datetime(df_Tarifas['Data_Referencia'], format='%Y/%m')
df_Tarifas.drop(columns = ['Receita_R$', 'Receita_Tributada_R$', 'Mes_Ano', 'Ano'], inplace = True)

# Changing units from BRL/MWh to BRL/kWh
df_Tarifas['Tarifa_Media_R$'] = (df_Tarifas['Tarifa_Media_R$']/1000).round(2)
df_Tarifas['Tarifa_Tributada_R$'] = (df_Tarifas['Tarifa_Tributada_R$']/1000).round(2)

##--------------------------------------------------------------------------------------------##
# Exporting DataFrames in .csv
df_Base.to_csv('Output/DataFrame_Base.csv', sep = ';', encoding = 'UTF-8', index = False)
df_Tarifas.to_csv('Output/DataFrame_Tarifas.csv', sep = ';', encoding = 'UTF-8', index = False)
print('\nOs DataFrames foram importados com sucesso.\n')