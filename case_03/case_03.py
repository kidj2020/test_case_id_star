import pandas as pd


pd.options.display.float_format = '{:,}'.format

#*  Step 1. Import file “Use_Case_3.txt”
df = pd.read_table('./data/Use_Case_3.txt', sep='|', header=0)

# print(df, '\n')
# print(df.dtypes)

def get_total_score(employee_detail):
    intercept_score = 33.53

    age_scores_weight = {
        0 : 13.45,
        21 : 17.88,
        30 : 18.98,
        51 : 19.33,
    }

    gender_scores_weight = {
        "Male" : 24.44,
        "Female": 21.89
    }

    occupation_scores_weight = {
        "Employee" : 12.45,
        "Entrepreneur" : 9.34,
        "Others" : 6.78
    }

    age_score = 0
    gender_score = 0
    occupation_score = 0

    for k, score in age_scores_weight.items():
        if employee_detail['Age'] >= k:
            age_score = score
    
    if employee_detail['Occupation'] in occupation_scores_weight:
        occupation_score = occupation_scores_weight[employee_detail['Occupation']]
    else:
        occupation_score = occupation_scores_weight['Entrepreneur']
        
    # print(f'{age_score=}')
    # print(f"gender_score={gender_scores_weight[employee_detail['Gender']]}")
    # print(f'{occupation_score=}', '\n')

    total_score = float(intercept_score + (1.24 * age_score) + (9.42 * gender_scores_weight[employee_detail['Gender']]) + (7.34 * occupation_score))

    return total_score

def get_risk_segment(total_score):
    segment = {
        379 : "Very Low Risk (VLR)",
        375 : "Low Risk (LR)",
        370 : "Medium Risk (MR)",
        350 : "High Risk (HR)",
        325 : "Very High Risk (VHR)",
        0 : "Very High Risk (VHR) 2",
    }

    for key, letter in segment.items():
        if total_score > key:
            return letter
    return "NaN"
    
def get_facility_limit(risk_segment, employee_detail):
    if risk_segment == "Very High Risk (VHR) 2":
        risk_segment = "Very High Risk (VHR)"
        
    income_multiplier = {
        "Very High Risk (VHR)": {
            "Employee": 1.5,
            "Self Employed": 1
        },
        "High Risk (HR)": {
            "Employee": 2,
            "Self Employed": 1.3
        },
        "Medium Risk (MR)": {
            "Employee": 3.5,
            "Self Employed": 1.5
        },
        "Low Risk (LR)": {
            "Employee": 6,
            "Self Employed": 3
        },
        "Very Low Risk (VLR)": {
            "Employee": 8,
            "Self Employed": 4
        },
    }
    
    return employee_detail['MonthlyIncome']*income_multiplier[risk_segment][employee_detail['Occupation']]


for index, row in df.iterrows():
    employee = df.loc[index].to_dict()
    #*  Step 2. Calculate the total score using the formula
    employee_total_score = get_total_score(employee)
    
    #*  Step 3. Determine the Risk Segment from the Total Score using the matrix 
    employee_risk_segment = get_risk_segment(employee_total_score)
    
    #* Step 4. Determine Income Multiplier and Calculate Facility Limit using the matrix 
    employee_facility_limit = get_facility_limit(employee_risk_segment, employee)
    
    # print(employee, '\n' )
    # print(f'total_score= {employee_total_score}')
    # print(f'{employee_risk_segment=}')
    # print(f'{employee_facility_limit=}')

    df.loc[index, 'TotalScore'] = employee_total_score
    df.loc[index, 'RiskSegment'] = employee_risk_segment
    df.loc[index, 'FacilityLimit'] = employee_facility_limit

print(df)



