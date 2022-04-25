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
print('\nA base de dados foi importada com sucesso.')

##--------------------------------------------------------------------------------------------##
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
df_Base.fillna({'UF': 'Não Informado', 'ID_UF': 0.0, 'ID_Municipio': 0.0}, inplace = True)
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

# Exporting DataFrames in .csv
df_Base.to_csv('Output/DataFrame_Base.csv', sep = ';', encoding = 'UTF-8', index = False)
print('\nOs DataFrames foram importados com sucesso.\n')