import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('/Users/thannarot/sig/cambodia-poverty-app/poverty_adm1.csv')
# Calculate new values directly from the existing columns
df['Education0'] = df['edu_attain']
df['edu_attain0'] = df['edu_attain']
df['edu_attend0'] = df['edu_attend']
df['Health0'] = df['Health0']
df['health_access0'] = df['health_acc']
df['health_food0'] = df['health_foo']
df['health_handwash0'] = df['health_han']
df['health_sanit0'] = df['health_san']
df['health_water0'] = df['health_wat']
df['LivingStandard0'] = df['LivingStan']
df['liv_asset0'] = df['liv_asset0']
df['liv_cooking0'] = df['liv_cookin']
df['liv_coping0'] = df['liv_coping']
df['liv_elect0'] = df['liv_elect0']
df['liv_hous0'] = df['liv_hous0']
df['liv_overcr0'] = df['liv_overcr']
df['Monetary0'] = df['Monetary0']
df['Unemploy0'] = df['unemploy0']
df['underemployment0'] = df['underemplo']
df['overall0'] = df['overall0']

# Columns to process
feat_names = ['Education0', 'Health0', 'LivingStandard0', 'Monetary0', 'Total', 'Unemploy0', 'edu_attain0', 
              'edu_attend0', 'health_access0', 'health_food0', 'health_handwash0', 'health_sanit0', 
              'health_water0', 'liv_asset0', 'liv_cooking0', 'liv_coping0', 'liv_elect0', 'liv_hous0', 
              'liv_overcr0', 'overall0', 'underemployment0', 'unemploy0']

# Initialize the result dictionary
res = {}

# Process each feature name
for feat_name in feat_names:
    _Deprived = []
    _Not_Deprived = []

    # Assuming 'Total' column exists and is calculated
    total = df['Total']
    obj = df[feat_name]
    
    for i in range(len(obj)):
        if total[i] != 0:
            _Not_Deprived.append(1 - (obj[i] / total[i]))
            _Deprived.append(obj[i] / total[i])
        else:
            # Handle the zero division case appropriately
            _Not_Deprived.append(1)  # Assuming a default value
            _Deprived.append(0)      # Assuming a default value

    # Store the results in the dictionary
    res[feat_name] = {
        "Not Deprived": _Not_Deprived,
        "Deprived": _Deprived,
    }

res["name_area"] = df['HRName'].tolist()
res["id_area"] = df['PRO_CODE'].tolist()
res["population"] = df['pop'].tolist()
res["buildings"] = df['building'].tolist()

# Save the result to a JSON file
with open("../povertymappingapp/static/data/VALNERABILITY_DATA_AMD1_v2.json", 'w', encoding='utf8') as f:
    json.dump(res, f, indent=4)

print("Processed data has been saved!")

