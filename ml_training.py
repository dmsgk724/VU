import torch
from torch import nn
import pandas as pd

# 1. choose ML model

# class customizedModel(nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.layer_1 = nn.Linear(in_features=4,out_features=3)
#         self.layer_2 = nn.Linear(in_features = 3, out_features=1)

#     def forward(self,x):
#         return self.layer_2(self.layer_1(x))
    
# model = customizedModel()




def prepare_data(data):
    train_X = data.drop(columns=["_id","ltable._id","ltable.PHONENUMBER","rtable._id","rtable.PHONENUMBER","gold"]).to_numpy()
    train_Y = data.gold.to_numpy()
    train_X = torch.from_numpy(train_X)
    train_Y = torch.from_numpy(train_Y)
    print(train_X)
    print(train_Y)
    return train_X, train_Y


train_data = pd.read_csv("restaurants1/csv_files/labeled_data.csv",header = 5)
train_X , train_Y = prepare_data(train_data)






# 2. Train a ML model using labeled_data.csv

# 3. Calculate 