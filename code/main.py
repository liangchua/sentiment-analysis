# Libraries

import altair as alt
import base64
import matplotlib.pyplot as plt
import nltk
import numpy as np
import os
import pandas as pd
import streamlit as st

from info import Info
from models import SentimentAnalysisModels
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from PIL import Image
from wordcloud import WordCloud

nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


#%% Static Path

# images
logo = Image.open('logo.png')
mask = np.array(Image.open('wordcloud-shape.png'))

# datasets
PRODUCT_REVIEWS_PATH = os.path.join(os.getcwd(), 'product-reviews.csv')
SOCMED_PATH = os.path.join(os.getcwd(), 'socmed-tweets.csv')
POLITIC_PATH = os.path.join(os.getcwd(), 'politic-uk.csv')
EMPLOYEE_PATH = os.path.join(os.getcwd(), 'employee-feedback.csv')
HEALTHCARE_PATH = os.path.join(os.getcwd(), 'healthcare-depression.csv')


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

# text data cleaning
def clean_text(text):
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [token for token in tokens if token not in stop_words and token.isalpha()]
    cleaned_text = " ".join(cleaned_tokens)
    return cleaned_text

# sentiment analysis models
def models(selected_model, text):
    if selected_model == 'TextBlob':
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

# set sidebar
with st.sidebar:
    # add logo
    sidecols = st.columns(3)
    with sidecols[1]:
        st.image(logo, width=90)
    
    # project overview
    st.write(' ')
    Info().overview()

# add pagination
tabs = st.tabs(['Analytics','Playground'])


#%% Tab 1: Sentiment Analysis with dataset

with tabs[0]:
    
    try:
        st.info('This tab allow you to upload a dataset to run the sentiment\
                analysis or you may choose the sample datasets provided.')
        
        # user selection (upload own dataset or preview with sample datasets)
        options = st.selectbox('Choose to upload a dataset or preview using sample dataset',
                               ['upload dataset','sample 1: product review',
                                'sample 2: social media', 'sample 3: political',
                                'sample 4: employee feedback', 'sample 5: healthcare'])
        
        if options == 'upload dataset':
            uploaded_data = st.file_uploader('Upload data here')
            data = pd.read_csv(uploaded_data, encoding='unicode_escape')
        # sample 1
        elif options == 'sample 1: product review':
            Info().prod_info()
            data = pd.read_csv(PRODUCT_REVIEWS_PATH, encoding='unicode_escape')
            data = data[['reviews.text']]
        # sample 2
        elif options == 'sample 2: social media':
            Info().socmed_info()
            data = pd.read_csv(SOCMED_PATH, encoding='unicode_escape')
            data = data[['text']]
        # sample 3
        elif options == 'sample 3: political':
            Info().politic_info()
            data = pd.read_csv(POLITIC_PATH)
            data = data[['text']][:round(len(data)*0.2)]
        # sample 4
        elif options == 'sample 4: employee feedback':
            Info().employee_info()
            data = pd.read_csv(EMPLOYEE_PATH, encoding='unicode_escape')
            data = data[['feedback']]
        # sample 5
        elif options == 'sample 5: healthcare':
            Info().healthcare_info()
            data = pd.read_csv(HEALTHCARE_PATH, encoding='unicode_escape')
            data = data[['clean_text']]
        st.write(' ')
        sample_select = st.radio('Choose a model',
                                 ['TextBlob','Vader','Pattern'], horizontal=True)
        st.write(' ')
        
        # ask user input "choose text column"
        prod_text_fea = st.selectbox('Choose the "text" column',
                                     data.columns)
        
        # add button "click to run the analysis"
        if st.button('Run Sentiment Analysis'):
            with st.spinner('In progress ...'):
                # run sentiment analysis
                data = data[[prod_text_fea]]
                data.columns = ['text']
                labels = []
                scores = []
                temp_text = []
                for text in data['text']:
                    # clean text
                    text = clean_text(text)
                    # get results
                    label, score = models(sample_select, text)
                    labels.append(label)
                    scores.append(score)
                else:
                    pass
                
                # add new features to dataset
                data['label'] = labels
                data['score'] = scores
                
                # total count by label
                cnt_fea = data['label'].value_counts()
                cnt_dic = {'POSITIVE':0, 'NEUTRAL':0, 'NEGATIVE':0}
                
                for key in cnt_dic.keys():
                    if key in cnt_fea.index:
                        cnt_dic[key] = cnt_fea[key]
                
                cnt_fea = pd.Series(cnt_dic)
                cnt_fea = cnt_fea.reset_index()
                cnt_fea.columns = ['label','count']
                
                with st.expander('Sentiment analysis results'):
                    # display results in table form
                    st.write(data)
                
                with st.expander('Total count of each label'):
                    # display total count of each label in table form
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
                
                with st.expander('Wordcloud and top occurance words'):
                    # get the clean text
                    data['cleaned_text'] = data['text'].apply(clean_text)
                    
                    # create word cloud for each label
                    labels = ['POSITIVE','NEUTRAL','NEGATIVE']
                    for label in labels:
                        # plot wordcloud
                        st.write(f"{label.title()} Sentiment Word Cloud")
                        label_data = data[data['label'] == label]
                        words = " ".join(list(label_data['cleaned_text']))
                        freq_dist = FreqDist(word_tokenize(words))
                        colors = ['white','yellow','red']
                        cmap = plt.cm.colors.ListedColormap(colors)
                        wordcloud = WordCloud(width=680, height=400, colormap=cmap,
                                              background_color=None, mask=mask
                                              ).generate_from_frequencies(freq_dist)
                        fig, ax = plt.subplots(facecolor='none')
                        ax.imshow(wordcloud, interpolation='lanczos')
                        ax.axis('off')
                        st.pyplot(fig)
                        
                        # display top 10 words
                        st.write(f" Top 10 {label.title()} Words")
                        word_df = pd.DataFrame.from_dict(freq_dist, orient='index', columns=['frequency'])
                        word_df = word_df.sort_values(by='frequency', ascending=False)
                        st.table(word_df.head(10))
                
                st.success('Done!')
            
        else:
            st.info('Click "Run Sentiment Analysis" to get sentiment analysis results')
    except:
        st.info('Please upload a dataset')


#%% Tab 2: Playground

with tabs[1]:
    
    st.info('This tab allow you to play with any sentences for sentiment analysis.')
    
    # get user input in text
    text = st.text_area('Type the text to analyze')
    
    # get user input of selected model
    selected_model = st.radio('Pick a model',['TextBlob','Vader','Pattern'], horizontal=True)
    st.write(' ')
    
    if st.button('Run Analysis'):
        with st.spinner('In progress ...'):
            # get sentiment analysis results
            label, score = models(selected_model, text)
            st.success('Done!')
            # display results
            st.write('Sentiment Label: ', label)
            st.write('Score: ', score)
    else:
        st.info('Click "Run Analysis" to get sentiment analysis results')










