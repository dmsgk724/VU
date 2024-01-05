import pandas as pd

#Step 1: Preparation of Data

def prepare_data():
    yelp_data = pd.read_csv("restaurants1/csv_files/yelp.csv")
    zomato_data = pd.read_csv("restaurants1/csv_files/zomato.csv")

    # Drop duplicates
    yelp_data = yelp_data.drop_duplicates()
    zomato_data = zomato_data.drop_duplicates()

    #Drop unwanted Columns

    #FormatLast name

    #FormatPhoneNumber


    #Clean NullValue




#Step 2: Blocking scheme


#Step 3: Identify duplicate and delete

#Step 4: Find perfect match and compare to ground truth


    
