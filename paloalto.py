import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import streamlit as st 
# data load 
file_address = r"C:\Users\Acer\Downloads\Palo Alto Networks (2).csv"
df = pd.read_csv(file_address)
# Remove duplicates
df.drop_duplicates(inplace=True)
# Missing values check
print(df.isnull().sum())
# Attrition mapping
df['Attrition'] = df['Attrition'].map({1: 'Yes', 0: 'No'})
# Education mapping
education_map = {
    1: 'Below College',
    2: 'College',
    3: 'Bachelor',
    4: 'Master',
    5: 'Doctor'
}
df['Education'] = df['Education'].map(education_map)
# Rating mapping
rating_map = {
    1: 'Low',
    2: 'Medium',
    3: 'High',
    4: 'Very High'
}
cols = [
    'EnvironmentSatisfaction',
    'JobSatisfaction',
    'RelationshipSatisfaction',
    'WorkLifeBalance'
]
for col in cols:
    df[col] = df[col].map(rating_map)
joblevel_map = {
    1: 'Entry Level',
    2: 'Junior Level',
    3: 'Mid Level',
    4: 'Senior Level',
    5: 'Executive Level'
}
df['JobLevel'] = df['JobLevel'].map(joblevel_map)

#Over time yes or no mapping
df['OverTime'] = df['OverTime'].str.lower().str.strip()
#data mapping complete and cleaning start 
# Lowercase convert
df['Department'] = df['Department'].str.lower()
df['JobRole'] = df['JobRole'].str.lower()

# Extra spaces remove
df['Department'] = df['Department'].str.strip()
df['JobRole'] = df['JobRole'].str.strip()
#unique value check
print(df['Department'].unique())
print(df['JobRole'].unique())
#print(df.dtypes)
#print(df.head())
# Overall Attrition Assessment
# Total employees
total = len(df)
print("Total Employee=",total)
# Employees  left
Employeesleft = df[df['Attrition'] == 'Yes'].shape[0]
print("Employees left=",Employeesleft)
# Attrition rate
attrition_rate = (Employeesleft / total) * 100
print("Attrition Rate:", attrition_rate)
# proportion 
proportion = df['Attrition'].value_counts(normalize=True) * 100
print(proportion)
#Baseline
baseline_turnover = (df['Attrition'] == 'Yes').mean() * 100
print(f"Baseline Turnover Rate: {baseline_turnover:.2f}%")

#role wise analysis 
dept_attrition = pd.crosstab(
    df['Department'], 
    df['Attrition'], 
    normalize='index'
) * 100

print(dept_attrition.round(1))

#highest fresquency exit
role_attrition_count = df[df['Attrition'] == 'Yes']['JobRole'].value_counts()
print(role_attrition_count.round(1))

#Combine both Department + Role:
pivot = pd.crosstab(
    [df['Department'], df['JobRole']],
    df['Attrition'],
    normalize='index'
) * 100
#Highlight functional areas with attrition concentration
pivot['Attrition Rate (%)'] = pivot['Yes']
print(pivot.sort_values(by='Attrition Rate (%)', ascending=False).head(10))
role_attrition_rate = pd.crosstab(
    df['JobRole'], 
    df['Attrition'], 
    normalize='index'
) * 100
print(role_attrition_rate)
print(pivot.round(1))

# Dynamically pick correct column-- Demographic Attrition Analysis
col = 'Yes' if 'Yes' in role_attrition_rate.columns else 'yes'

role_attrition_rate['Attrition Rate (%)'] = role_attrition_rate[col]

print(role_attrition_rate[['Attrition Rate (%)']].sort_values(by='Attrition Rate (%)', ascending=False))

bins = [18, 25, 35, 45, 55, 65]
labels = ['18-25', '26-35', '36-45', '46-55', '55+']

df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

age_attrition = pd.crosstab(
    df['AgeGroup'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in age_attrition.columns else 'yes'
age_attrition['Attrition Rate (%)'] = age_attrition[col]

print(age_attrition[['Attrition Rate (%)']])

# gender wise 
gender_attrition = pd.crosstab(
    df['Gender'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in gender_attrition.columns else 'yes'
gender_attrition['Attrition Rate (%)'] = gender_attrition[col]

print(gender_attrition[['Attrition Rate (%)']])

# marital status 
marital_attrition = pd.crosstab(
    df['MaritalStatus'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in marital_attrition.columns else 'yes'
marital_attrition['Attrition Rate (%)'] = marital_attrition[col]

print(marital_attrition[['Attrition Rate (%)']])


df['Education'] = df['Education'].map(education_map)
edu_attrition = pd.crosstab(
    df['Education'], 
    df['Attrition'], 
    normalize='index'
) * 100
#tenure 
# attrition year at company 
bins = [0, 2, 5, 10, 20, 40]
labels = ['0-2 yrs', '3-5 yrs', '6-10 yrs', '11-20 yrs', '20+ yrs']

df['TenureGroup'] = pd.cut(df['YearsAtCompany'], bins=bins, labels=labels)

tenure_attrition = pd.crosstab(
    df['TenureGroup'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in tenure_attrition.columns else 'yes'
tenure_attrition['Attrition Rate (%)'] = tenure_attrition[col]

print(tenure_attrition[['Attrition Rate (%)']])
#carrer stage se attrition 

def career_stage(years):
    if years <= 3:
        return 'Early Career'
    elif years <= 10:
        return 'Mid Career'
    else:
        return 'Senior'

df['CareerStage'] = df['TotalWorkingYears'].apply(career_stage)

career_attrition = pd.crosstab(
    df['CareerStage'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in career_attrition.columns else 'yes'
career_attrition['Attrition Rate (%)'] = career_attrition[col]

print(career_attrition[['Attrition Rate (%)']])

# promotion by attrition 
bins = [0, 1, 3, 5, 10, 20]
labels = ['0-1 yr', '2-3 yrs', '4-5 yrs', '6-10 yrs', '10+ yrs']

df['PromotionGap'] = pd.cut(df['YearsSinceLastPromotion'], bins=bins, labels=labels)

promo_attrition = pd.crosstab(
    df['PromotionGap'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in promo_attrition.columns else 'yes'
promo_attrition['Attrition Rate (%)'] = promo_attrition[col]

print(promo_attrition[['Attrition Rate (%)']])

# overtime attrition 
overtime_attrition = pd.crosstab(
    df['OverTime'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in overtime_attrition.columns else 'yes'
overtime_attrition['Attrition Rate (%)'] = overtime_attrition[col]

print(overtime_attrition[['Attrition Rate (%)']])

#ravel attrition
travel_attrition = pd.crosstab(
    df['BusinessTravel'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in travel_attrition.columns else 'yes'
travel_attrition['Attrition Rate (%)'] = travel_attrition[col]

print(travel_attrition[['Attrition Rate (%)']])


#ditance from attrion
bins = [0, 5, 10, 20, 50]
labels = ['0-5 km', '6-10 km', '11-20 km', '20+ km']

df['DistanceGroup'] = pd.cut(df['DistanceFromHome'], bins=bins, labels=labels)
distance_attrition = pd.crosstab(
    df['DistanceGroup'], 
    df['Attrition'], 
    normalize='index'
) * 100

col = 'Yes' if 'Yes' in distance_attrition.columns else 'yes'
distance_attrition['Attrition Rate (%)'] = distance_attrition[col]

print(distance_attrition[['Attrition Rate (%)']])
#kpi 
total_employees = len(df)
left_employees = df[df['Attrition'] == 'Yes'].shape[0]

attrition_rate = (left_employees / total_employees) * 100
print("Attrition Rate:", round(attrition_rate, 1), "%")

dept_attrition = pd.crosstab(
    df['Department'],
    df['Attrition'],
    normalize='index'
) * 100

print(dept_attrition.round(1))

role_attrition = pd.crosstab(
    df['JobRole'],
    df['Attrition'],
    normalize='index'
) * 100
print(role_attrition.round(1))

early_attrition = df[df['YearsAtCompany'] <= 2]

rate = (early_attrition[early_attrition['Attrition'] == 'Yes'].shape[0] /
        early_attrition.shape[0]) * 100
print("Early Tenure Attrition:", round(rate, 1), "%")

overtime_attrition = pd.crosstab(
    df['OverTime'],
    df['Attrition'],
    normalize='index'
) * 100
print(overtime_attrition.round(1))
