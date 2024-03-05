import streamlit as st
import os
import pandas as pd
import json
from pandas.errors import ParserError



#---------------------------------------------------



def upload_file():

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        return uploaded_file 
    else:
        st.write('Waiting for the file....')


#---------------------------------------------------


def check_uploaded_file(uploaded_file):


  

    if uploaded_file is not None:
    # Display the file format
        file_extension = uploaded_file.name.split('.')[-1].lower()
        st.write(f"Uploaded file format: {file_extension}")
        file_path = os.path.join("uploads", uploaded_file.name)
    
        
        


#---------------------------------------------------



def upload_file_in_db(uploaded_file,file_path):

    if uploaded_file is not None:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)  

        # Create the directory if it doesn't exist
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.write(f"File saved to: {file_path}")

        # Can be used wherever a "file-like" object is accepted:
        st.success('File uploaded', icon="✅")


#---------------------------------------------------


def read_dataset(file_extension,uploaded_file,file_path):
     #Create DataFrame acording the file format

    #To read XLSX file
    if file_extension == "xlsx":
        dataframe = pd.read_excel(uploaded_file)


    #To read CSV file
    elif file_extension == "csv":
        dataframe = pd.read_csv(uploaded_file)

        
    #To read JSON file
    elif file_extension == "json":
            
    # Read JSON data from file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            dataframe = pd.DataFrame(data,index = list(data.keys()))


    #To read TEXT file
    elif file_extension == "txt":
            try:
                dataframe = pd.read_csv(uploaded_file, sep='\t')
            except ParserError:
                 st.error('Your data is in Unstructured format!!\n  Refresh and try again after structuring your data')
                 st.stop()
    st.write(dataframe)
    return dataframe



#---------------------------------------------------




def separate_features(dataframe):

    features = dataframe.columns.to_list()
    categorical_features = [feature for feature in dataframe.columns if dataframe[feature].dtypes == 'O' or len(dataframe[feature].unique()) < 25]
    numerical_features = [feature for feature in dataframe.columns if dataframe[feature].dtypes != 'O' or len(dataframe[feature].unique()) > 25]
    return features,categorical_features,numerical_features




def get_target(features,dataframe) -> str :
    
    target = None
    target = st.multiselect("Select the Target Feature",features, max_selections = 1)
    if len(target):
        y = dataframe[target[0]]

        return target[0]
    else:
        st.write('Waiting for the target selection....')
        



def get_user_features(independent_features,preferrence):

    if preferrence == 'Default':
        return [independent_features,len(independent_features)]
    elif preferrence == 'Manual':
        preferred = st.radio(
        'Select your preferrence',
        options = ["Selct Number of Features", "Select Own features"],
        captions = ["Features with high correlation will be selected(recommended)", "Select the preferred features"])
        if preferred == "Selct Number of Features":
            number = st.number_input("Enter number of fatures to be used", value=None, placeholder="Type a number...",step = 1)

            return [independent_features,number]
            
        else:
            selected_independent_features = st.multiselect("Select the prefered features",independent_features)
            return [selected_independent_features,len(selected_independent_features)]



def user_preferrence():
    preferred = st.radio(
        "How do you prefer feature selection?",
        ["Default", "Manual"],
        captions = ["Features will be selected automatically (recommended)", "Select your own features"],
        horizontal = True)
    return preferred




def check_problem_type(dataframe,target,user_preferred_features,number):

    n = len(dataframe[target].unique())
    if n < 25 :
        st.write("It is a Classification Dataset")
        return True if len(user_preferred_features) else False

    else:
        st.write("It is a Regression Dataset")
        return True if len(user_preferred_features) else False

    