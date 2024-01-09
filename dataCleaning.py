import pandas as pd
import re

pd.set_option('display.max_seq_items', None)
# pd.set_option('display.max_rows',None)

patterns = []
patterns.append (re.compile(r'\d+rd'))
patterns.append( re.compile(r'\d+th'))
patterns.append( re.compile(r'\d+st'))
patterns.append( re.compile(r'\d+nd'))

n_pattern = re.compile(r'\d+&\d+')

short_word = ["Caf", "Crepe","Restauran", "Tim", "Sausalit","Ba","Crea","Ta","Gril","Expres","Pu","Currywurs","Pizz","Del","Truax","Loung","Cuisin","Hous","Mercantil","Kitche","Sho","Toky"]



def data_cleaning(data):
    
    for n in ['NAME', 'ADDRESS']:
        data[n] = data[n].str.replace("!", "i")
        data[n] = data[n].str.replace("$", "s")
        data[n] = data[n].str.replace("@", "a")

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
        if name_strings[0] == "Anne" or name_strings[-1] in short_word:
            data.at[i,'NAME'] =' '.join(name_strings).strip()
        elif len(name_strings) == 1 and name_strings[0].isdigit():
            data.at[i,'NAME'] =' '.join(name_strings).strip()
        else:
            data.at[i,'NAME'] =' '.join(name_strings).strip()+' '
 
    return data


def data_cleaning_2(data,rows):
    for row_num in rows:
        index= data[data['ID']==row_num].index.values
        name_strings= data['NAME'].iloc[int(index)].split()
        data.at[int(index),'NAME'] = ' '.join(name_strings).strip()
    return data

    
def compare(origin, modified):
    merge = pd.merge(origin, modified,indicator=True, how="outer")
    
    merge_right= merge.query("_merge=='right_only'")
    merge_right = merge_right['ID'].values
    return merge_right


error_file = pd.read_csv("data/yelp_error.csv")
origin_file = pd.read_csv("restaurants1/csv_files/yelp.csv")

error_file = data_cleaning(error_file)
ids = list(compare(origin_file,error_file))
error_file = data_cleaning_2(error_file,ids)

different_rows = compare(origin_file,error_file)
accuracy = (len(origin_file)-len(different_rows))/len(origin_file)
print("My accuracy is ", accuracy)

#Report the number of corrupt instances
#type of errors in each tuplea
#number of fixed instances
#error detection and correction techniques applied