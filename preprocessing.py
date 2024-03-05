import streamlit as st
def start_preprocessing(user_dataframe,number):
    if number is not None:
        st.write(number)
        st.write(user_dataframe)
    else:
        st.write("Select the number of features...")



def fill_null_categorical(dataframe,feature):
    dataframe[feature] = dataframe[feature].fillna(dataframe[feature].mode())
    return dataframe[feature]