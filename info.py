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
                        There are total of 2 tabs created in this project. The "Analytics"\
                        allow users to upload a dataset to run the sentiment analysis. Besides,\
                        users can choose the sample datasets for preview, which includes\
                        "Product Review", "Social Media", "Political Sentiment Analysis"\
                        , "Employee Feedback Analysis" and "Healthcare Reviews Analysis".\
                        The another tab allow users to play with different sentiment analysis\
                        algorithms by just typing a random sentence.* ####
                    ''')
    
    def prod_info(self):
        
        st.info('**Potential Analysis:**\
                Business could analyze customer feedback to identify common themes\
                and issues with their products. They could use this information to\
                improve product quality, identify potential product features, and \
                adjust pricing strategies based on customer satisfaction. Additionally,\
                businesses could compare customer reviews levels across different \
                products and use this information to prioritize resources and \
                investments in different products lines. By identifying common themes\
                in customer feedback, businesses could take targeted action to improve\
                product quality and overall customer satisfaction.')
    
    def socmed_info(self):
        
        st.info('**Potential Analysis:**\
                Businesses or organizations could analyze public sentiment about their\
                brand, product, or topic on social media to identify potential issues\
                or opportunities for engagement. They could use this information to \
                adjust their marketing or communication strategies, respond to customer\
                feedback, or address issues in real-time. Additionally, businesses could\
                track changes in public sentiment over time and compare sentiment levels\
                across different topics or brands to gain insights into broader trends\
                or patterns in public opinion. By analyzing public sentiment on social\
                media, businesses can better understand customer perceptions and take\
                targeted action to improve brand reputation and customer satisfaction.')
    
    def politic_info(self):
        
        st.info('**Potential Analysis:**\
                Political campaigns or organizations could analyze public sentiment\
                about political candidates or issues on social media to identify\
                potential issues or opportunities for engagement. They could use\
                this information to adjust their messaging, respond to public feedback\
                or address concerns in real-time. Additionally, they could track\
                changes in public sentiment over time and compare sentiment levels\
                accross different candidates or issues to gain insights into broader\
                trends or patterns in public opinion. By analyzing public sentiment\
                on social media, political campaigns or organization can better \
                understand public perceptions and take targeted action to improve\
                their chances of success.')
    
    def employee_info(self):
        
        st.info('**Potential Analysis:**\
                Companies could analyze employee feedback to identify common themes\
                and issues related to employee satisfaction, such as management\
                style, work-life balance, or compensation. They could use this\
                information to improve company policies, address employee concerns,\
                and enhance overall employee satisfaction. Additionally, companies\
                could compare employee satisfaction across different departments\
                or locations and use this information to prioritize resources and\
                investments in different areas of the organization. By identifying\
                common themes in employee feedback, companies can take targeted action\
                to improve employee satisfaction, reduce employee turnover, and create\
                a positive workplace culture.')
    
    def healthcare_info(self):
        
        st.info('**Potential Analysis:**\
                Healthcare providers could analyze patient feedback to identify areas\
                for improvement, such as communication with patients, wait times, or\
                overall experience. They could also track changes in patient\
                satisfaction over time and compare satisfaction levels accross\
                different hospitals. By analyzing common themes in patient feedback,\
                healthcare providers could take targeted action to improve patient\
                experience and overall satisfaction.')
