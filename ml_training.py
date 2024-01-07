
import pandas as pd
from difflib import SequenceMatcher
import sklearn.svm as svm
import sklearn.metrics as mt
from sklearn.model_selection import cross_val_score, cross_validate

# 1. prepare training data and preprocess predictX.csv

def prepare_input(data):
    train_X = []
    for x in data:
        name_score = SequenceMatcher(None, x[0], x[2]).ratio()
        address_score = SequenceMatcher(None, x[1], x[3]).ratio()
        train_X.append([name_score, address_score])
    return train_X

# for training data
train_data = pd.read_csv("restaurants1/csv_files/labeled_data.csv",header = 5)
raw_train_X = train_data.drop(columns=["_id","ltable._id","ltable.PHONENUMBER","rtable._id","rtable.PHONENUMBER","gold"]).values
x = prepare_input(raw_train_X)
y = list(train_data['gold'].values)

# 2. Train a ML model using labeled_data.csv for three times
svm_model = svm.SVC(kernel = 'linear')
svm_model.fit(x,y) # training using labeled_data.csv
scores = cross_val_score(svm_model, x, y, cv=3)
print('My cross validation is ', scores.mean())

# 3. Predict using predictX.csv and calculate accuracy using goldY.csv
# for predicting data
predicting_data = pd.read_csv("data/predictX.csv").values
predicting_x = prepare_input(predicting_data)
true_data = pd.read_csv("data/goldY.csv").values

prediction = svm_model.predict(predicting_x)
print(mt.accuracy_score(list(prediction),list(true_data)))