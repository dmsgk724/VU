import pandas as pd
import numpy as np
import collections 
from difflib import SequenceMatcher
import re
from itertools import combinations,product

#Step 1: Preparation of Data

def prepare_data(yelp_data, zomato_data):


    # Drop ratings and number of Reviews
    yelp_data = yelp_data.drop(columns=["RATING","NO_OF_REVIEWS"])
    zomato_data = zomato_data.drop(columns=["RATING","NO_OF_REVIEWS"])


    # Drop duplicates
    yelp_data = yelp_data.drop_duplicates()
    zomato_data = zomato_data.drop_duplicates()

    #lower str name
    yelp_data['NAME'] = yelp_data['NAME'].map(str.lower)
    zomato_data['NAME'] = zomato_data['NAME'].map(str.lower)


    #lower str address
    yelp_data['ADDRESS'] = yelp_data['ADDRESS'].map(str.lower)
    zomato_data['ADDRESS'] = zomato_data['ADDRESS'].map(str.lower)

    # address에서 쉼표 제거하기 
    yelp_data['ADDRESS'] = yelp_data['ADDRESS'].str.replace(",", "")
    zomato_data['ADDRESS'] = zomato_data['ADDRESS'].str.replace(",", "")
    yelp_data['ADDRESS'] = yelp_data['ADDRESS'].str.replace(".", "")
    zomato_data['ADDRESS'] = zomato_data['ADDRESS'].str.replace(".", "")
    

        #regular expresion of phone number
    standard = re.compile('\(\d\d\d\)\s\d\d\d\-\d\d\d\d')

    for datasets in [yelp_data, zomato_data]:
        for index, row in datasets.iterrows():
            #check typo in phonenumber
            if standard.match(row['PHONENUMBER']) == None:
                datasets.drop(index,inplace=True)
                
    
    return yelp_data, zomato_data


yelp = pd.read_csv("restaurants1/csv_files/yelp.csv")
zomato= pd.read_csv("restaurants1/csv_files/zomato.csv")
yelp,zomato = prepare_data(yelp,zomato)



#Step 2: Blocking scheme
def blocking(df):
    blocks = collections.defaultdict(list)

    for index, row in df.iterrows():
        title = row['NAME'][:3]
        blocks[title].append(row)

    return blocks


 
#Step 3: Identify duplicate and delete

    #group마다 pair를 matcher를 통해 비교하고 threshold넘기면 하나의 데이터 셋에서 그 row삭제한다.
    #그 pair가 labeled dataset에 있으면 있는 count증가
    #아니면 아닌 count증가
def del_duplicate(blocks):
    for key,block in blocks.items():
        pair = list(combinations(block,2))
        del_list = set()
        for y, z in pair:
            score = SequenceMatcher(None, y['NAME'], z['NAME']).ratio()
            score += SequenceMatcher(None, y['PHONENUMBER'], z['PHONENUMBER']).ratio()
            score += SequenceMatcher(None, y['ADDRESS'], z['ADDRESS']).ratio()
            if score >= 2.5:
                del_list.add(z['ID'])
        new_block = []
        for row in block:
            if row['ID'] in del_list:
                continue
            new_block.append(row)
        blocks[key] = new_block
    return blocks

#Step 4: Find perfect match and compare to ground truth
match_list = set()
no_match_list = set()

#block 1-> zomato block2-> yelp 
def find_perfect_match(block1,block2):
    pair = list(product(block1,block2))
    for y, z in pair:
        score = SequenceMatcher(None, y['NAME'], z['NAME']).ratio()
        score += SequenceMatcher(None, y['PHONENUMBER'], z['PHONENUMBER']).ratio()
        score += SequenceMatcher(None, y['ADDRESS'], z['ADDRESS']).ratio()
        if score >= 2.1:
           # print(y['ID'])
            match_list.add((int(y['ID'])-1450000000000,int(z['ID'])-1445980000001))
        if score < 2.1:
            no_match_list.add((int(y['ID'])-1450000000000,int(z['ID'])-1445980000001))



def compute_accuracy():

    correct = 0
    wrong = 0
    labeled_data = pd.read_csv("restaurants1/csv_files/labeled_data.csv",header=5)
    for e in match_list:
        ltable_id ,rtable_id = e
        condition = ((labeled_data['ltable._id']==ltable_id ) & (labeled_data['rtable._id']==rtable_id) )
        if labeled_data[condition].empty==1:
            continue
        else: 
            selected_rows = labeled_data[condition].iloc[0]
            #print(selected_rows)
            
            if selected_rows['gold']==1:
                #print("correct")
                correct +=1
            elif selected_rows['gold']==0:
                wrong +=1
    print(correct)
    print(wrong)
    for e in no_match_list:
        ltable_id ,rtable_id = e
        condition = ((labeled_data['ltable._id']==ltable_id )& (labeled_data['rtable._id']==rtable_id) )
        if labeled_data[condition].empty==1:
            continue
        else: 
            selected_rows = labeled_data[condition].iloc[0]
            #print(selected_rows)
        
            if selected_rows['gold']==1:
                
                wrong +=1
            elif selected_rows['gold']==0:
                correct +=1
    
    
    accuracy = float(correct/(correct+wrong))
    print("Our accuracy is: " + str(accuracy))

    



block_yelp = blocking(yelp)
block_zomato = blocking(zomato)
clean_yelp = del_duplicate(block_yelp)
clean_zomato = del_duplicate(block_zomato)


for key, block in clean_yelp.items():
    if key in clean_zomato:
        find_perfect_match(block_zomato[key],block)

print(len(match_list), len(no_match_list))

compute_accuracy()
