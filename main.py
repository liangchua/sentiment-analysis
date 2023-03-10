# Libraries

import base64
import pandas as pd
import streamlit as st
import os

from info import Info
from models import SentimentAnalysisModels
from PIL import Image


#%% Static Path

# images path
logo = Image.open('logo.png')

PRODUCT_REVIEWS_PATH = os.path.join(os.getcwd(), 'product-reviews.csv')


# # resize images
# with Image.open('bg6.png') as im:
#     resized_im = im.resize((1920, 1080))
#     resized_im.save('bg6-resized.png')

# simple, brand, customer, market, politics, healtcare


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
    
    selected_model = st.radio('Pick a model',['DistilBERT','TextBlob',
                                              'Vader','Pattern'], horizontal=True)
    st.write(' ')
    
    if st.button('Run Analysis'):
        with st.spinner('In progress ...'):
            # time.sleep(2)
            label, score = models(selected_model, text)
            st.success('Done!')
            st.write(label, score)
    else:
        st.info('Click "Run Analysis" to get sentiment analysis results')


#%% Tab 2: Product Reviews

with tabs[1]:
    
    Info().tab1_info()
    
    options = st.selectbox('Choose to upload dataset or preview using sample dataset',
                           ['upload dataset','sample dataset'])
    if options == 'upload dataset':
        uploaded_data = st.file_uploader('Upload data here')
        
        if uploaded_data:
            upload_select = st.radio('Select a model',['DistilBERT','TextBlob',
                                                      'Vader','Pattern'], horizontal=True)
            st.write(' ')
            
            
            
    else:
        sample_select = st.radio('Choose a model',['DistilBERT','TextBlob',
                                                  'Vader','Pattern'], horizontal=True)
        
        data = pd.read_csv(PRODUCT_REVIEWS_PATH, encoding='unicode_escape')
        data = data[['brand','categories','reviews.text']][:50]
        
        st.table(data.head())
        
        


#%% Tab 3: Social Media

with tabs[2]:
    
    Info().tab2_info()

#%% Tab 4: Political 

with tabs[3]:
    
    Info().tab3_info()

#%% Tab 5: Employee 

with tabs[4]:
    
    Info().tab4_info()


#%% Tab 6: Healthcare

with tabs[5]:
    
    Info().tab5_info()










