import sqlite3
import pandas as pd
import numpy as np
import pprint
import re

#* Step 1. Import file “Use_Case_1.txt”
df = pd.read_table('./data/Use_Case_1.txt', sep=',', index_col=1)

#FILTERING ACTIVE LOAN
df_active = df.query("Active == 'Y'")

key_active_list = df_active.index.values.tolist()

df_year_month = df_active.filter(regex=re.compile(r'tahunBulan\d\d', re.IGNORECASE))


dt_dict = {}
#* Step 2. Find number of active facilities which have DPD>30 or Collectability>2 in the last 2 years
#Converting column based on tahunbulan to dictionary
for index, row in df_year_month.iterrows():
    # print(f"{index}----------")

    dpd = -1
    collectability = -1
    year_month = -1

    series = '01'
    dt_dict[index] = []
    for col_name in df_year_month.columns:
        dt_year = {}
        # print(f"{col_name}: {row[col_name]}")
        series_col = str(''.join(filter(str.isdigit, col_name)))
        m = re.search(r'\d\d$', col_name)

        if str(col_name).lower().endswith('kol'):
            collectability = row[col_name]

        if str(col_name).lower().endswith('ht'):
            dpd = row[col_name]

        if m:
            year_month = row[col_name]

        if dpd != -1 and collectability != -1 and year_month != -1:
            dt_year[year_month] = {'dpd': dpd, 'col' : collectability}
            dt_dict[index].append(dt_year)
            series = series_col
            dpd = -1
            collectability = -1
            year_month = -1
    

# pprint.pprint(dt_dict, indent=2)

# ITERATING DICTIONARY for counting 
dt_result = {}
for k,v in dt_dict.items():
    count = 0
    for row in v:
        for x,y in row.items():
            if y['dpd'] > 30 or y['col'] > 2:
                count+=1
    dt_result[k] = count
    # print(f'{k}:\t{count}')   

# pprint.pprint(dt_result)
for i in key_active_list:
    df.loc[i,'activity_result'] = dt_result[i]
    # print(dt_result[i])

# df['activity_result'] = df['activity_result'].apply(np.int64) 
df['activity_result'] = df['activity_result'].fillna(0).astype(int)

print(df[['jeniskredit','activity_result']].dropna())