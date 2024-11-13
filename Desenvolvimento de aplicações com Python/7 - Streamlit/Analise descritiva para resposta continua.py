import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

import streamlit as st
import time


#Função que Filtra o DataFrame
@st.cache_data
def filter (df):
    
    ''' Função para filtrar as informações do DataFrame '''
    
    df = df.drop(['Unnamed: 0', 'index'], axis = 1)
    df['data_ref'] = pd.to_datetime(df['data_ref'])
    df_new = df.dropna().reset_index(drop=True)
    return df_new


#Função cria todos os gráficos estabilidade
@st.cache_data
def point(_df):
    
    ''' Recebe um Dataframe, filtra as variáveis categóricas e retorna
    todos os pointplots da renda média em função do tempo para a distribuição das variáveis da lista '''
    
    var_qualitativo = _df.select_dtypes(exclude=['int64','float64', 'datetime']).columns   

    for var in var_qualitativo:
        
        st.markdown(f'#### Estabilidade da variável explicativa {var} ao longo do tempo:')
        
        fig, ax = plt.subplots(figsize=(20,5))
            
        sns.pointplot(data=previsao_renda_filter,
                    x = 'data_ref',
                    y = 'renda',
                    hue = var,
                    dodge = True,
                    errorbar = ('ci', 95),
                    ax=ax
                    )

        tick_data = previsao_renda_filter['data_ref'].map(lambda data: data.strftime('%m/%Y')).unique()

        tick_data.tolist()

        ticks = ax.set_xticks(list(range(previsao_renda_filter['data_ref'].nunique())))
        labels = ax.set_xticklabels(tick_data, rotation=45)

        plt.xlabel('Tempo')
        plt.ylabel('Média Renda ($)')
        plt.legend(bbox_to_anchor = (1.05, 1),
                    loc = 2,
                    borderaxespad = 0,
                    title = var.capitalize()
                    )

        st.pyplot(fig)
        
#Função cria gráfico estabilidade  
def point_unico(_var: str):
    
    ''' Recebe a string de uma variável categórica e retorna
    um pointplot da renda média em função do tempo para a distribuição da variável '''
    
    if _var == 'sexo':
        st.markdown('##### Estabilidade da variável explicativa sexo ao longo do tempo:')
        
    elif _var == 'posse_de_veiculo':
        st.markdown('##### Estabilidade da variável explicativa posse_de_veiculo ao longo do tempo:')
        
    elif _var == 'posse_de_imovel':
        st.markdown('##### Estabilidade da variável explicativa posse_de_imovel ao longo do tempo:')

    elif _var == 'tipo_renda':
        st.markdown('##### Estabilidade da variável explicativa tipo_renda ao longo do tempo:')
        
    elif _var == 'educacao':
        st.markdown('##### Estabilidade da variável explicativa educacao ao longo do tempo:')
        
    elif _var == 'estado_civil':
        st.markdown('##### Estabilidade da variável explicativa estado_civil ao longo do tempo:')
        
    elif _var == 'tipo_residencia':
        st.markdown('##### Estabilidade da variável explicativa tipo_residencia ao longo do tempo:')
        
    elif _var == 'mau':
        st.markdown('##### Estabilidade da variável explicativa mau ao longo do tempo:')

    fig, ax = plt.subplots(figsize=(20,5))
            
    sns.pointplot(data=previsao_renda_filter,
                x = 'data_ref',
                y = 'renda',
                hue = _var,
                dodge = True,
                errorbar = ('ci', 95),
                ax=ax
                )

    tick_data = previsao_renda_filter['data_ref'].map(lambda data: data.strftime('%m/%Y')).unique()

    tick_data.tolist()

    ticks = ax.set_xticks(list(range(previsao_renda_filter['data_ref'].nunique())))
    labels = ax.set_xticklabels(tick_data, rotation=45)

    plt.xlabel('Tempo')
    plt.ylabel('Média Renda ($)')
    plt.legend(bbox_to_anchor = (1.05, 1),
                loc = 2,
                borderaxespad = 0,
                title = _var.capitalize()
                )

    st.pyplot(fig)

#Configuração da página    
st.set_page_config(page_title = 'Análise Descritiva',
                   page_icon='https://cdn-icons-png.freepik.com/512/8649/8649621.png',
                    layout='wide')


#Leitura do DataFrame
previsao_renda = pd.read_csv('previsao_de_renda.csv')
#Filtrando o DataFrame
previsao_renda_filter = filter(previsao_renda)

metadados = pd.DataFrame({'dtypes': previsao_renda_filter.dtypes}) #Cria o dataframe dos metadados
metadados['missing'] = previsao_renda_filter.isna().sum()
metadados['perc_missing'] = round((metadados['missing']/previsao_renda_filter.shape[0])*100)
metadados['valores_unicos'] = previsao_renda_filter.nunique()


st.title('Análise Descritiva Para Resposta Contínua:')
st.markdown('----')

left_column, right_column = st.columns(2) #Cria duas colunas

with left_column: #Utiliza a coluna da esquerda
    st.markdown('#### Dataframe utilizado:')
    st.markdown('Dataframe interativo completo.')
    if st.checkbox('Exibir o DataFrame'): #Exibe o dataframe quando o checkbox é selecionado
        previsao_renda_filter  #Exibe o dataframe com magic

with right_column: #Utiliza a coluna da direita
    st.markdown('#### Metadados do Dataframe:')
    st.markdown('O Dataframe abaixo contém os metadados de todas as variáveis do Dataframe utilizado.')
    if st.checkbox('Exibir os metadados do DataFrame'): #Exibe o dataframe dos metadados quando o checkbox é selecionado
        metadados   #Exibe o dataframe com magic
st.markdown('----')
        


st.markdown('### Gráficos da distribuição ao longo do tempo das variáveis qualitativas:')
st.markdown('''Para os seguintes gráficos o eixo X apresenta o tempo análisado e o eixo Y pode variar entre uma contagem
            de quantidade total, uma contagem sobreposta ou a quantidade normalizada em porcentagem. ''')
st.markdown(' ')

st.sidebar.markdown('### Gráficos da distribuição ao longo do tempo das variáveis qualitativas:')    


if st.sidebar.checkbox('Exibir todas as variáveis'): #Visualização gráfica de todas as variáveis categóricas filtradas
    
    var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64','float64', 'datetime']).columns #Filtra as variáveis categóricas
    
    chosen_comp = st.sidebar.radio(  #Opções de visualização dos gráficos
        'Escolha como observar as distribuições:',
        ('Empilhada', 'Sobreposta', 'Porcentagem')
    )
    
    st.sidebar.markdown('----')

    #Troca do ingles para português na sidebar
    if chosen_comp == 'Empilhada':
        chosen_comp = 'center'
    elif chosen_comp == 'Sobreposta':
        chosen_comp = 'layered'
    elif chosen_comp == 'Porcentagem':
        chosen_comp = 'normalize'   
    
    for var in var_qualitativo: #Loop for para criação de todos os gráficos
        
        tab_freq = pd.crosstab(previsao_renda_filter['data_ref'],previsao_renda_filter[var])
        st.markdown(f'#### Distribução ao longo do tempo da variável explicativa {var}:')
        st.bar_chart(tab_freq, x_label='Data', y_label='Contagem',stack=chosen_comp) #Gráfico interativo com streamlit
    
else: #Continua para a configuração de somente 1 gráfico
    
    var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64','float64', 'datetime']).columns #Filtra as variáveis categóricas
            
    selectbox_var_comp = st.sidebar.selectbox( #Seleção da variável a ser exibida
        'Escolha a variável:',
        (var_qualitativo)
    )
    
    tab_freq = pd.crosstab(previsao_renda_filter['data_ref'],previsao_renda_filter[selectbox_var_comp])

    #Seleciona o titulo a ser mostrado 
    if selectbox_var_comp == 'sexo':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa sexo:')
        
    elif selectbox_var_comp == 'posse_de_veiculo':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa posse_de_veiculo:')
        
    elif selectbox_var_comp == 'posse_de_imovel':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa posse_de_imovel:')

    elif selectbox_var_comp == 'tipo_renda':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa tipo_renda:')
        
    elif selectbox_var_comp == 'tipo_renda':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa tipo_renda:')
        
    elif selectbox_var_comp == 'educacao':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa educacao:')
        
    elif selectbox_var_comp == 'estado_civil':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa estado_civil:')
        
    elif selectbox_var_comp == 'tipo_residencia':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa tipo_residencia:')
        
    elif selectbox_var_comp == 'mau':
        st.markdown('##### Distribuição ao longo do tempo da variável explicativa mau:')

    chosen = st.sidebar.radio( #Opções de visualização dos gráficos
        'Escolha como quer observar a distribuição:',
        ('Empilhada', 'Sobreposta', 'Porcentagem')
    )

    #Troca do inglês para o português
    if chosen == 'Empilhada':
        chosen = 'center'
    elif chosen == 'Sobreposta':
        chosen = 'layered'
    elif chosen == 'Porcentagem':
        chosen = 'normalize'    

    st.bar_chart(tab_freq, x_label='Data', y_label='Contagem',stack=chosen) #Gráfico interativo com streamlit

    if st.sidebar.checkbox('Comparar com outra variável?'): #Opção no menu para comparação com outra variável
        
        var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64','float64', 'datetime']).columns #Filtra as variáveis categóricas
            
        selectbox_var_comp = st.sidebar.selectbox( #Seleção da variável a ser comparada
            'Escolha da variável:',
            (var_qualitativo)
        )
                    
        tab_freq = pd.crosstab(previsao_renda_filter['data_ref'],previsao_renda_filter[selectbox_var_comp])

        #Seleciona o titulo a ser mostrado 
        if selectbox_var_comp == 'sexo':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa sexo:')
        
        elif selectbox_var_comp == 'posse_de_veiculo':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa posse_de_veiculo:')
        
        elif selectbox_var_comp == 'posse_de_imovel':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa posse_de_imovel:')

        elif selectbox_var_comp == 'tipo_renda': 
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa tipo_renda:')
        
        elif selectbox_var_comp == 'tipo_renda':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa tipo_renda:')
        
        elif selectbox_var_comp == 'educacao':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa educacao:')
        
        elif selectbox_var_comp == 'estado_civil':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa estado_civil:')
        
        elif selectbox_var_comp == 'tipo_residencia':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa tipo_residencia:')
        
        elif selectbox_var_comp == 'mau':
            st.markdown('##### Distribuição ao longo do tempo da variável explicativa mau:')

        chosen_comp = st.sidebar.radio( #Opções de visualização dos gráficos
            'Escolha como quer observar a distribuição: ',
            ('Empilhada', 'Sobreposta', 'Porcentagem')
        )

        #Troca do inglês para o português
        if chosen_comp == 'Empilhada':
            chosen_comp = 'center'
        elif chosen_comp == 'Sobreposta':
            chosen_comp = 'layered'
        elif chosen_comp == 'Porcentagem':
            chosen_comp = 'normalize'    


        st.bar_chart(tab_freq, x_label='Data', y_label='Contagem',stack=chosen_comp) #Gráfico interativo com streamlit
        
    st.markdown('----')
    st.sidebar.markdown('----')
    
st.markdown('### Gráficos da estabilidade das variáveis qualitativas ao longo do tempo:')
st.markdown('''Para os seguintes gráficos analisa-se a estabilidade das variáveis. 
            Utilizando a variáção da renda média ao longo do tempo para a variável selecionada.''')
st.sidebar.markdown('### Gráficos da estabilidade das variáveis qualitativas ao longo do tempo:')

#Barra de carregamento para efeitos visuais
texto_progresso = 'Carregando...'
my_bar = st.progress(0, text=texto_progresso)

for i in range(100):
    time.sleep(0.01)
    my_bar.progress(i + 1, text=texto_progresso)
time.sleep(1)
my_bar.empty()

if st.sidebar.checkbox('Exibir todas as variáveis '): #Visualização gráfica de todas as variáveis categóricas filtradas
          
    point(previsao_renda_filter) #Utilização da função que plota todos os gráficos de estabilizade de todas as variáveis categóricas filtradas do Dataframe
    
else:
    
    var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64','float64', 'datetime']).columns #Filtra as variáveis categóricas
            
    selectbox_var_est = st.sidebar.selectbox( #Seleção da variável a ser exibida
        'Escolha a variável: ',
        (var_qualitativo)
    )
        
    point_unico(selectbox_var_est) #Utilização da função que plota o gráfico de estabilidade da variável selecionada

    

    if st.sidebar.checkbox('Comparar com outra variável? '): #Opção no menu para comparação com outra variável
        
        var_qualitativo = previsao_renda_filter.select_dtypes(exclude=['int64','float64', 'datetime']).columns #Filtra as variáveis categóricas
            
        selectbox_var_comp_est = st.sidebar.selectbox( #Seleção da variável a ser comparada
            'Escolha da variável:',
            (var_qualitativo)
        )
        
        point_unico(selectbox_var_comp_est) #Utilização da função que plota o gráfico de estabilidade da variável selecionada para comparação
        
st.sidebar.markdown('----')        
st.sidebar.button('Recarregar')    