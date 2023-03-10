# Libraries

import streamlit as st


#%% Class for information

class Info:
    
    def __inti__(self):
        ...
    
    def overview(self):
        
        st.info('''
                    ### Project Overview
                    
                    #### *This sentiment analysis project aims to develop an automated\
                        system that can accurately classify the sentiment of textual\
                        data. The problem statement is that manually analyzing large\
                        volume of data is time-consuming and error-prone. Therefore,\
                        the purpose of this project is to develop a machine learning\
                        model that can accurately identify positive, negative and neutral\
                        sentiments in text data. The benefits of this project include\
                        reducing the time and effort required to analyze large volume\
                        of data, providing accurate insights into customer sentiment\
                        and improving decision-making in various industris such as \
                        marketing, finance and politics.\
                        There are total of 5 tabs created in this project. The "testing"\
                        tab allow users to try on each sentiment analysis model, while the\
                        other four tabs are the sample use cases of sentiment analysis such\
                        as "Product Review", "Social Media", "Political Sentiment Analysis"\
                        , "Employee Feedback Analysis" and "Healthcare Reviews Analysis".* ####
                    ''')
