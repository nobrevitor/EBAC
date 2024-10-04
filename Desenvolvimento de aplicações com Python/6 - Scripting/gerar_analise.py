import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plota_pivot_table(df, value, index, func, ylabel, xlabel, title, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    return None

if len(sys.argv) < 2:
    print('\n Quantidade de argumentos insuficientes')
    sys.exit()

print('\n Nome do script: ', sys.argv[0], '\n')

meses = sys.argv[1:13]

for mes in meses:

    print(' Mês de refência:', mes)

    sinasc = pd.read_csv('./input/SINASC_RO_2019_'+mes+'.csv')


    max_data = sinasc.DTNASC.max()[:7]
    print(' ', max_data, '\n')

    os.makedirs('./output_script/Gráficos/'+max_data, exist_ok=True)

    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'Média idade mãe', 'Data nascimento', 'Média idade mãe X Data nascimento')
    plt.savefig('./output_script/Gráficos/'+max_data+'/Média idade mãe por data.png')

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'Média idade mãe', 'Data de nascimento', 'Média idade mãe X Sexo', 'unstack')
    plt.savefig('./output_script/Gráficos/'+max_data+'/Média idade mãe por sexo.png')

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'Média peso do bebe', 'Data de nascimento', 'Média peso do bebê X Sexo', 'unstack')
    plt.savefig('./output_script/Gráficos/'+max_data+'/Média peso bebe por sexo.png')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'Peso mediano', 'Escolaridade mãe', 'Peso mediano X Escolaridade mãe', 'sort')
    plt.savefig('./output_script/Gráficos/'+max_data+'/Peso mediano por escolaridade mãe.png')

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'APGAR1 médio', 'Gestação', 'Média APGAR1 X Gestação', 'sort')
    plt.savefig('./output_script/Gráficos/'+max_data+'/Média APGAR1 por gestação.png')
