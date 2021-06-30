import string
import pandas as pd
from fastai.learner import load_learner
import sys

sys.path.append("/home/ubuntu/miniconda3/lib/python3.8/site-packages/")
sys.path.append("/home/ubuntu/miniconda3/lib/python3.8/site-packages/pandas/")

class Answor:
    def __init__(self):
        self.labels = self._get_categories()
        self.learner = load_learner('assets/10epoch-oversampling-classifier.pkl')        
        
    def remove_punctuation(self, text):
        text = ''.join([c for c in text if c not in string.punctuation])
        return text

    def clean_text(self, text):
        if len(text) == 0:
            return None
        
        t = self.remove_punctuation(text)
        t = t.lower()
        print(t)
        return t

    def _get_categories(self):
        category_names = pd.read_csv('assets/labels.csv', header=None)
        category_names.columns=['category']
        c_names = category_names.sort_values('category', ascending=True)
        c_names = c_names['category'].tolist()
        return c_names

    def get_prediction(self, question):
        
        q = self.clean_text(question)
        if q == None:
            return 'None', 0.0
        
        result = self.learner.predict(q)
        # result structure: category number, tensor([category index]), tensor([probabilities array])
        category = int(result[0]) - 1 # convert back to index
        probability = result[2].tolist()[category]
        category_name = self.labels[category]
        return category_name, probability
    
# get_prediction('is covid survivable without ventilators')