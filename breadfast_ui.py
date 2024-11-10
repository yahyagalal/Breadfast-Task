import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


def calculate_days_coverage(demand_df, invent_df):

    demand_df.columns = ['id', 'date', 'fore_sales']
    invent_df.columns = ['id', 'batch_id', 'expiry_date', 'inventory']
    demand_df['date'] = demand_df['date'].apply(convert_to_datetime)
    invent_df['date'] = invent_df['expiry_date'].apply(convert_to_datetime)
    demand_df.sort_values(by=['id','date'], inplace=True)
    invent_df.sort_values(by=['id', 'expiry_date'], inplace=True)
    product_ids=demand_df['id'].unique()
    days_forward_list=[]

    
    for i in product_ids:
        single_demand_df=demand_df[demand_df['id']==i]
        single_invent_df=invent_df[invent_df['id']==i].copy()
        days_forward=0
        
        for demand_idx, demand in single_demand_df.iterrows():
        
            fore_sales=demand['fore_sales']
            date=demand['date']        
            single_invent_df=single_invent_df[single_invent_df['expiry_date']>=date]  
                
            for invent_idx, invent in single_invent_df.iterrows():
                if(invent['inventory']<fore_sales):
                    fore_sales -= invent['inventory']
                    single_invent_df.at[invent_idx, 'inventory'] = 0
                else:
                    single_invent_df.at[invent_idx, 'inventory'] -= fore_sales
                    fore_sales=0
                    break
        
        
            if(fore_sales==0):
                days_forward+=1
            else:
                break
    
        days_forward_list.append(days_forward)

    return pd.DataFrame(data= {"id":product_ids, "days_coverage":days_forward_list})
        



        
def convert_to_datetime(input_date):
    if isinstance(input_date, datetime):
        return input_date 
    else:
        return datetime.strptime(input_date, '%d-%m-%Y')
        



    
            
    

st.title('CSV Processing Application')

uploaded_file1 = st.file_uploader("Upload the first CSV", type='csv')
uploaded_file2 = st.file_uploader("Upload the second CSV", type='csv')

if uploaded_file1 and uploaded_file2:
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)
    
    st.write("First CSV Data:")
    st.write(df1)
    
    st.write("Second CSV Data:")
    st.write(df2)
    
    result_df = calculate_days_coverage(df1, df2)
    
    st.write("Processed DataFrame:")
    st.write(result_df)
else:
    st.write("Please upload two CSV files.")
