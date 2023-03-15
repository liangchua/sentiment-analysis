# Libraries

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pattern.en import sentiment
from textblob import TextBlob
# from transformers import pipeline


#%% Pre-trained sentiment analysis models

class SentimentAnalysisModels:
    
    def __init__(self, text):
        self.text = text
    
    def TextBlob(self):
        blob = TextBlob(self.text)
        result = blob.sentiment.polarity
        
        if result >= 0.1:
            label = 'POSITIVE'
        elif result <= -0.1:
            label = 'NEGATIVE'
        else:
            label = 'NEUTRAL'
        
        return label, result
    
    def Vader(self):
        analyzer = SentimentIntensityAnalyzer()
        result = analyzer.polarity_scores(self.text)
        
        if result['neu'] >= 0.8:
            label = 'NEUTRAL'
            score = result['neu']
        elif result['neu'] < 0.8 and result['neg'] > result['pos']:
            label = 'NEGATIVE'
            score = result['neg']
        else:
            label = 'POSITIVE'
            score = result['pos']
        
        return label, score
    
    def Pattern(self):
        result = sentiment(self.text)
        
        if result[0] >= 0.1:
            label = 'POSITIVE'
        elif result[0] <= -0.1:
            label = 'NEGATIVE'
        else:
            label = 'NEUTRAL'
        
        return label, result[0]
    
    # def HuggingFaceTransformer(self):
    #     nlp = pipeline('sentiment-analysis')
    #     result = nlp(self.text)
        
    #     if result[0]['score'] >= -0.1 and result[0]['score'] <= 0.1:
    #         label = 'NEUTRAL'
    #         return label, result[0]['score']
    #     else:
    #         return result[0]['label'], result[0]['score']


