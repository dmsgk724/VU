import pandas as pd
import re

pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_rows',None)

patterns = []
patterns.append (re.compile(r'\d+rd'))
patterns.append( re.compile(r'\d+th'))
patterns.append( re.compile(r'\d+st'))
patterns.append( re.compile(r'\d+nd'))

n_pattern = re.compile(r'\d+&\d+')

def data_cleaning(data):
    
    for n in ['NAME', 'ADDRESS']:
        data[n] = data[n].str.replace("!", "i")
        data[n] = data[n].str.replace("$", "s")
        data[n] = data[n].str.replace("@", "a")
        
    #숫자 3을 e로 바꿔야 한다.
    #103을 10E로 어떻게 바꾸징 ㅎㅎ
    cnt = 0
    for i, row in data.iterrows():
        address_strings = row['ADDRESS'].split()
        for arr_index, x in enumerate(address_strings):
            if x=='&' or n_pattern.match(x):
                continue
            else :
                address_strings[arr_index]=address_strings[arr_index].replace('&','n')
            if (x.isdigit()):
                continue
            else : 
                next = 0
                for pattern in patterns:
                    if pattern.match(address_strings[arr_index]):
                        next = 1
                if (next==1):
                    continue
                else:
                    address_strings[arr_index]=address_strings[arr_index].replace('3','e')
                    address_strings[arr_index]=address_strings[arr_index].replace('9','g')
        
        name_strings = row['NAME'].split()
        for arr_index, x in enumerate(name_strings):
            if x=='&' or n_pattern.match(x):
                continue
            else :
                name_strings[arr_index]=name_strings[arr_index].replace('&','n')
            if(x.isdigit()):
                continue
            else : 
                next = 0
                for pattern in patterns:
                    if pattern.match(name_strings[arr_index]):
                        next = 1
                if (next==1):
                    continue
                else:
                    name_strings[arr_index]=name_strings[arr_index].replace('3','e')
                    name_strings[arr_index]=name_strings[arr_index].replace('9','g')
        data.at[i,'ADDRESS'] =' '.join(address_strings).strip()
        if name_strings[-1] == "Caf" or name_strings[-1] == "Crepe" or name_strings[-1] == "Restauran" or name_strings[-1] == "Tim" or name_strings[-1] == "Sausalit" or name_strings[-1] == "Ba" or name_strings[-1] == "Crea" or name_strings[-1] == "Ta" or name_strings[0] == "Anne":
            data.at[i,'NAME'] =' '.join(name_strings).strip()
        elif len(name_strings) == 1 and name_strings[0].isdigit():
            data.at[i,'NAME'] =' '.join(name_strings).strip()
        else:
            data.at[i,'NAME'] =' '.join(name_strings).strip()+' '
   # print(data)
    

    

    

    
    return data
                

    
def compare(origin, modified):
    merge = pd.merge(origin, modified,indicator=True, how="outer")
    print(merge[merge['_merge']=='right_only'])
    #print(merge[merge['_merge']=='left_only']) #456개 다르다
    #print(merge[merge['_merge']=='both']) #현재까지 5409개 찾음 


error_file = pd.read_csv("/Users/parkeunha/DataIntegrationAndAnalysis/data/yelp_error.csv")
origin_file = pd.read_csv("/Users/parkeunha/DataIntegrationAndAnalysis/restaurants1/csv_files/yelp.csv")

error_file = data_cleaning(error_file)
compare(origin_file,error_file)
#print(error_file.iloc[5])
#print(origin_file.iloc[5])




#Report the number of corrupt instances
#type of errors in each tuplea
#number of fixed instances
#error detection and correction techniques applied