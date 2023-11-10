import pandas as pd


pd.options.display.float_format = '{:,}'.format

#* Step 3. Import file “Use_Case_2.txt”
df = pd.read_table('./data/Use_Case_2.txt', sep='|', header=0)

# print(df)
# print(df.dtypes)

#*  Step 4.     Find the Installment Amount.
for index, row in df.iterrows():
    #*  If Facility Type is Credit Card, then Monthly Installment Amount is 10% of Plafond
    if df.loc[index,'FacilityType'] == 'Credit Card':
        df.loc[index, 'Installment'] = df.loc[index,'Plafond'] * 10/100
    #*  otherwise:
    else:
        monthly_interest_rate = df.loc[index, 'PercentageOfAnnualInterestRate'] / 12
        monthly_installment_amount = df.loc[index,'Plafond'] * ( ((monthly_interest_rate/100 * pow((1 + monthly_interest_rate/100), df.loc[index,'Tenor']))) / ((pow((1 + monthly_interest_rate/100), df.loc[index,'Tenor'])) - 1) )
        df.loc[index, 'Installment'] = monthly_installment_amount

df['Installment'] = df['Installment'].fillna(0).astype('Float64')
# pd.options.display.float_format = '{:,}'.format
print(df,'\n---------------------------------------')

#*  Step 5. Find the percentage of DBR using the formula:
for index, row in df.iterrows():
    df.loc[index, 'PercentageOfDBR'] = (df.loc[index, 'Installment'] / df.loc[index, 'MonthlyIncome']) * 100

print(df)