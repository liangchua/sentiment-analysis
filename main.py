# Libraries

import altair as alt
import base64
import pandas as pd
import streamlit as st
import os
import re

from info import Info
from models import SentimentAnalysisModels
from PIL import Image
from sklearn.model_selection import train_test_split


#%% Static Path

# images path
logo = Image.open('logo.png')

PRODUCT_REVIEWS_PATH = os.path.join(os.getcwd(), 'product-reviews.csv')
SOCMED_PATH = os.path.join(os.getcwd(), 'socmed-tweets.csv')
POLITIC_PATH = os.path.join(os.getcwd(), 'politic-uk.csv')
EMPLOYEE_PATH = os.path.join(os.getcwd(), 'employee-feedback.csv')
HEALTHCARE_PATH = os.path.join(os.getcwd(), 'healthcare-depression.csv')

# # resize images
# with Image.open('bg6.png') as im:
#     resized_im = im.resize((1920, 1080))
#     resized_im.save('bg6-resized.png')


#%% Functions

# change background
def add_bg(image_file):
    with open(image_file,'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
                background-size: cover;
                }}
            </style>
            """,
            unsafe_allow_html=True
            )

# sentiment analysis models
def models(selected_model, text):
    if selected_model == 'DistilBERT':
        label, score = SentimentAnalysisModels(text).HuggingFaceTransformer()
    elif selected_model == 'TextBlob':
        label, score = SentimentAnalysisModels(text).TextBlob()
    elif selected_model == 'Vader':
        label, score = SentimentAnalysisModels(text).Vader()
    elif selected_model == 'Pattern':
        label, score = SentimentAnalysisModels(text).Pattern()
    return label, score

#%% User Interface (streamlit apps)

# set webpage title and icon
st.set_page_config(page_title="Sentiment Analysis Apps", page_icon=logo)

# set background
add_bg('bg6-resized.png')

# customization of other components with CSS
st.markdown(
    """
    <style>
    
    /* tab's background setting */
    button[data-baseweb="tab"] {
        background-color: #383838;
        width: 110px;
        height: 30px;
        border-radius: 15px 15px 0 0;
        }
    
    /* tab's font setting */
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
        font-weight: bold;
        }
    
    /* sidebar's font setting */
    div[class="css-k7vsyb e16nr0p31"] > h4 > em {
        font-size: 12px;
        }
    
    /* sidebar st.info color setting */
    div[class="stAlert"] > div[role="alert"] {
        background-color: #000000;
        border-radius: 15px 15px 15px 15px;
        }
    
    /* table's even columns setting */
    table td:nth-child(even) {
        background-color: #383838 !important;
        font-size: 12px !important;
        }
    
    /* table's odd columns setting */
    table td:nth-child(odd) {
        background-color: #232323 !important;
        font-size: 12px !important;
        }
    
    /* table's setting */
    table th{
        background-color: #838996 !important;
        color: white !important;
        font-size: 12px !important;
        font-weight: bold !important;
        }
    
    </style>
    """,
    unsafe_allow_html=True
)

# set page header with logo
st.markdown("""# 👍😍😑😡👎 Sentiment Analysis""")

# set sidebar header
with st.sidebar:
    
    sidecols = st.columns(3)
    with sidecols[1]:
        st.image(logo, width=90)
    
    # project overview
    st.write(' ')
    Info().overview()

# add pagination
tabs = st.tabs(['Testing','Product Review','Social Media','Politic','Employee',
                'Healthcare'])


#%% Tab 1: Sentence

with tabs[0]:
    
    st.info('This tab allow user to test with different sentiment analysis algorithms.')
    
    text = st.text_area('Text to analyze')
    
    selected_model = st.radio('Pick a model',['TextBlob','Vader','Pattern','DistilBERT'], horizontal=True)
    st.write(' ')
    
    if st.button('Run Analysis'):
        with st.spinner('In progress ...'):
            label, score = models(selected_model, text)
            st.success('Done!')
            st.write(label, score)
    else:
        st.info('Click "Run Analysis" to get sentiment analysis results')


#%% Tab 2: Product Reviews

with tabs[1]:
    
    # try:
        Info().tab1_info()
        
        options = st.selectbox('Choose to upload product review dataset or preview using sample dataset',
                               ['upload dataset','sample dataset'])
        
        if options == 'upload dataset':
            uploaded_data = st.file_uploader('Upload data here')
            data = pd.read_csv(uploaded_data, encoding='unicode_escape')
        else:
            data = pd.read_csv(PRODUCT_REVIEWS_PATH, encoding='unicode_escape')
            data = data[['brand','categories','reviews.text']]
            sample_data, remain_data = train_test_split(data, train_size=1000, random_state=0)
        
        st.write(' ')
        sample_select = st.radio('Choose a model for product reviews sentiment analysis',
                                 ['TextBlob','Vader','Pattern','DistilBERT'], horizontal=True)
        st.write(' ')
        
        prod_text_fea = st.selectbox('Choose the text feature from product review dataset',
                                     sample_data.columns)
        
        if st.button('Run Product Review Sentiment Analysis'):
            with st.spinner('In progress ...'):
                # run sentiment analysis
                labels = []
                scores = []
                for text in sample_data[prod_text_fea]:
                    # remove emoji
                    text = re.sub('[\U00010000-\U0010ffff]', ' ', text)
                    # remove all non-alphanumeric characters
                    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
                    # run sentiment analysis
                    label, score = models(sample_select, text)
                    labels.append(label)
                    scores.append(score)
                else:
                    pass
                
                # add new features to dataset
                sample_data['label'] = labels
                sample_data['score'] = scores
                
                st.success('Done!')
                
                # total count by label
                cnt_fea = sample_data['label'].value_counts()
                
                cnt_dic = {'POSITIVE':0, 'NEUTRAL':0, 'NEGATIVE':0}
                
                for key in cnt_dic.keys():
                    if key in cnt_fea.index:
                        cnt_dic[key] = cnt_fea[key]
                
                cnt_fea = pd.Series(cnt_dic)
                cnt_fea = cnt_fea.reset_index()
                cnt_fea.columns = ['label','count']
                
                with st.expander('Sentiment analysis results'):
                    st.write(sample_data)
                
                with st.expander('Total count of each label'):
                    # display results in table form
                    st.table(cnt_fea)
                    
                    cnt_cols = st.columns([1,3,1])
                    with cnt_cols[1]:
                        # calculate and display percentage of total
                        chart = alt.Chart(cnt_fea).transform_joinaggregate(
                            TotalCount='sum(count)',
                            ).transform_calculate(
                                percent_of_total='datum.count/datum.TotalCount'
                                ).mark_bar().encode(
                                    alt.X('percent_of_total:Q', axis=alt.Axis(format='.0%')),
                                    y='label:N',
                                    color=alt.value('#838996'),)
                        chart = chart.configure(background='#383838')
                        st.altair_chart(chart)
                
                with st.expander('Filter by other features'):
                    
                    agg_data = sample_data.groupby(['categories','label']).size().reset_index(name='count')
                    chart2 = alt.Chart(agg_data).mark_bar().encode(
                        y=alt.Y('categories:N'),
                        x=alt.X('count:Q', stack='normalize'),
                        color='label:N'
                        ).properties(width=680)
                    chart2 = chart2.configure(background='#383838')
                    st.altair_chart(chart2)
                    
                    agg_data2 = sample_data.groupby(['brand','label']).size().reset_index(name='count')
                    chart3 = alt.Chart(agg_data2).mark_bar().encode(
                        y=alt.Y('brand:N'),
                        x=alt.X('count:Q', stack='normalize'),
                        color='label:N'
                        ).properties(width=680)
                    chart3 = chart3.configure(background='#383838')
                    st.altair_chart(chart3)
                
        else:
            st.info('Click "Run Analysis" to get sentiment analysis results')
        
        
        
    # except:
    #     st.info('Please upload a dataset')


#%% Tab 3: Social Media

with tabs[2]:
    
    try:
        Info().tab2_info()
        
        options = st.selectbox('Choose to upload social media dataset or preview using sample dataset',
                               ['upload dataset','sample dataset'])
        
        if options == 'upload dataset':
            uploaded_data = st.file_uploader('Upload data here')
            data = pd.read_csv(uploaded_data, encoding='unicode_escape')
        else:
            data = pd.read_csv(SOCMED_PATH, encoding='unicode_escape')
            data = data[:50]
        
        st.write(' ')
        sample_select = st.radio('Choose a model for social media sentiment analysis',
                                 ['TextBlob','Vader','Pattern','DistilBERT'], horizontal=True)
        st.write(' ')
        st.table(data.head())
    except:
        st.info('Please upload a dataset')


#%% Tab 4: Political 

with tabs[3]:
    
    try:
        Info().tab3_info()
        
        options = st.selectbox('Choose to upload political dataset or preview using sample dataset',
                               ['upload dataset','sample dataset'])
        
        if options == 'upload dataset':
            uploaded_data = st.file_uploader('Upload data here')
            data = pd.read_csv(uploaded_data, encoding='unicode_escape')
        else:
            data = pd.read_csv(POLITIC_PATH)
            data = data[:50]
        st.write(' ')
        sample_select = st.radio('Choose a model for political sentiment analysis',
                                 ['TextBlob','Vader','Pattern','DistilBERT'], horizontal=True)
        st.write(' ')
        st.table(data.head())
    except:
        st.info('Please upload a dataset')


#%% Tab 5: Employee 

with tabs[4]:
    
    try:
        Info().tab4_info()
        
        options = st.selectbox('Choose to upload employee feedback dataset or preview using sample dataset',
                               ['upload dataset','sample dataset'])
        
        if options == 'upload dataset':
            uploaded_data = st.file_uploader('Upload data here')
            data = pd.read_csv(uploaded_data, encoding='unicode_escape')
        else:
            data = pd.read_csv(EMPLOYEE_PATH, encoding='unicode_escape')
            data = data[:50]
        st.write(' ')
        sample_select = st.radio('Choose a model for employee feedback sentiment analysis',
                                 ['TextBlob','Vader','Pattern','DistilBERT'], horizontal=True)
        st.write(' ')
        st.table(data.head())
    except:
        st.info('Please upload a dataset')


#%% Tab 6: Healthcare

with tabs[5]:
    
    try:
        Info().tab5_info()
        
        options = st.selectbox('Choose to upload healthcare dataset or preview using sample dataset',
                               ['upload dataset','sample dataset'])
        
        if options == 'upload dataset':
            uploaded_data = st.file_uploader('Upload data here')
            data = pd.read_csv(uploaded_data, encoding='unicode_escape')
        else:
            data = pd.read_csv(HEALTHCARE_PATH, encoding='unicode_escape')
            data = data[:50]
        st.write(' ')
        sample_select = st.radio('Choose a model for healthcare sentiment analysis',
                                 ['TextBlob','Vader','Pattern','DistilBERT'], horizontal=True)
        st.write(' ')
        st.table(data.head())
    except:
        st.info('Please upload a dataset')










