import glob
import string
import pandas as pd
from fastai.learner import load_learner

class Answor:
    def __init__(self):
        self.df_labels = self._get_categories()
        self.predictors = self._load_models()

    def _load_models(self):
        path = r'assets'
        all_files = glob.glob(path + "/tc_*.pkl")
        predictors ={}
        
        for fname in all_files:
            predictor = load_learner(fname)
            file_name = fname.split('/')[1]
            file_name_no_ext = file_name.split('.')[0]
            predictors[file_name_no_ext] = predictor
            
        return predictors
        
    def _remove_punctuation(self, text):
        text = ''.join([c for c in text if c not in string.punctuation])
        return text

    def _clean_text(self, text):
        if len(text) == 0:
            return None
        
        t = self._remove_punctuation(text)
        t = t.lower()
        print(t)
        return t

    def _get_categories(self):
        df_categories = pd.read_csv('assets/labels.csv')
        
        return df_categories

    def get_prediction(self, question):
        
        q = self._clean_text(question)
        if q == None:
            return 'None', 0.0

        best_prediction = {"category": '', "probability" : -0.1}
        best_predictor = ''

        for fname, predictor in self.predictors.items():
            result = predictor.predict(q)
            predicted_cid = int(result[0])
            # result structure: cid, tensor([category index]), tensor([probabilities array])
            # e.g. ('45', tensor(0), tensor([9.9725e-01, 4.1547e-05, 7.6428e-04, 1.9412e-03]))
            tensor_index = int(result[1])
            probability = result[2].tolist()[tensor_index]

            row = self.df_labels[self.df_labels['cid'] == predicted_cid]
            category_name = row['label'].values[0]
            cid = row['cid'].values[0]

            print('{} - {}, {}, {}'.format(fname, category_name, probability, cid))

            if probability > best_prediction["probability"]:
                best_prediction["probability"] = probability
                best_prediction["category"] = category_name
                best_predictor = fname

        print(best_prediction, best_predictor)
        return best_prediction
    
# get_prediction('is covid survivable without ventilators')