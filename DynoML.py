# Importing the required packages

import streamlit as st
import pandas as pd
from io import StringIO
import os
import json
from pandas.errors import ParserError
from script_functions import *
from preprocessing import *

# Defining the App title

st.title('DynoML')

# File uploader

uploaded_file = upload_file()

# Check for the file upload status
check_uploaded_file(uploaded_file)


if uploaded_file is not None:
    file_path = os.path.join("uploads", uploaded_file.name)
    file_extension = uploaded_file.name.split('.')[-1].lower()

# Upload file in the DataBase
    upload_file_in_db(uploaded_file,file_path)
        # Read the Dataset in DataFrame

    dataframe = read_dataset(file_extension,uploaded_file,file_path)





    if dataframe is not None:
        # Separate the dataset features
        features, categorical_features, numerical_features = separate_features(dataframe)

    # Select the Target Feature
        target = get_target(features,dataframe)

        # Get the independent features
        independent_features =  None
        if target is not None:
            independent_features = [ feature for feature in features if feature not in target ]


    # User selection
    if target is not None:
        preferrence = user_preferrence()
    
    user_preferred_features = None
    number = None
        # Feature selection acording to the user
    if independent_features is not None:
        l = get_user_features(independent_features,preferrence)
        user_preferred_features, number = l[0],l[1]
        if number is not None:
            st.write("The number of selected features:",number)

        # Get the dataframe with the selected features
    user_dataframe = None
    if user_preferred_features is not None:
        user_dataframe = dataframe[user_preferred_features]
        if len(user_preferred_features):
            st.write("The selected features",user_dataframe)

        # Check the type of problem
    if user_dataframe is not None:
        if check_problem_type(dataframe,target,user_preferred_features,number):
            if st.button('Start Preprocessing'):
                start_preprocessing(user_dataframe,number)