import pandas as pd
import streamlit as st
from io import BytesIO
from pycaret.classification import load_model, predict_model


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def main():
    st.set_page_config(
        page_title='PyCaret',
        layout="wide",
        initial_sidebar_state='expanded'
    )

    st.write("## Escorando o modelo gerado no PyCaret")
    st.markdown("---")

    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank Credit Dataset", type=['csv', 'ftr'])

    if data_file_1 is not None:
        if data_file_1.name.endswith('.csv'):
            df_credit = pd.read_csv(data_file_1)
        elif data_file_1.name.endswith('.ftr'):
            df_credit = pd.read_feather(data_file_1)

        if len(df_credit) > 50000:
            df_credit = df_credit.sample(50000, random_state=42)

        model_saved = load_model('model_final_pycaret')
        predict = predict_model(model_saved, data=df_credit)

        # Exibir as 5 primeiras linhas do resultado
        st.write("### Preview dos dados preditos")
        st.dataframe(predict.head())

        df_xlsx = to_excel(predict)

        st.download_button(
            label='📥 Download',
            data=df_xlsx,
            file_name='predict.xlsx'
        )



if __name__ == '__main__':
    main()









