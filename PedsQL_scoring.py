##This code normalizes the pedsql questionnaire of a subject

## Property of Anne-Lise Marais, 2024 {maraisannelise98@gmail.com}

##scripted on ipython

##requirements
## pip install pandas
## pip intall numpy

#before running the script
#change path line 31 and 77
#change subjectt name line 29

##Input configuration
#input should be a xlsx file named pedsql-subjectname
#input should have 21 columns and 2 rows. 
#The first row contains column names, the second row subject score
#Column names : physical1,physical2,physical3,physical4,physical5,physical6,physical7,physical8,emotion1,emotion2,emotion3,emotion4,emotion5,relation1,relation2,relation3,relation4,relation5,school1,school2,school3

import pandas as pd
import numpy as np
import os


#MAIN

#add your subject name
sub = 'sub-01'
    
rawpedsql_path = f'Documents/pedsql_{sub}.xlsx'
            
# If xlsx exist, proceed, otherwise stop
if os.path.exists(rawpedsql_path):
    rawdata = pd.read_excel(rawpedsql_path, header=0)
    #check data validity 
    all_valid = rawdata.apply(lambda col: col.map(lambda x: pd.isna(x) or (isinstance(x, (int, float)) and x in {0, 1, 2, 3, 4}))).all().all()
    
    # Verification of results
    if not all_valid:
        print("Some values are false, please check your data; it should only contain 0, 1, 2, 3, or 4.")
        exit()
        
    #create a copy of the df
    rawpedsql = rawdata.copy()

    #get each question names by scale, in a list
    q_physical = [f'physical{i}' for i in range(1, 9)]
    q_emotion = [f'emotion{i}' for i in range(1, 6)]
    q_relation = [f'relation{i}' for i in range(1, 6)]
    q_school = [f'school{i}' for i in range(1, 4)]
    #put all question names in a list

    # Define the replacement mapping for normalization, rate 100 if parent answered 0...
    mapping = {0:100, 1:75, 2:50, 3:25, 4:0}

    # Apply mapping
    pedsql_mapped = rawpedsql.replace(mapping)

    #Copy df
    pedsql = pedsql_mapped.copy()

    #extract psychosocial items (all except physical)
    psychosocial = pedsql_mapped.loc[:, ~pedsql_mapped.columns.str.contains('physical')]

    #rate scales, if a response if missing, it returns a NaN instead of the rounded mean
    #applies rounded mean on data only if at least half of the questions from the scale are answered
    pedsql['total'] = pedsql_mapped.apply(lambda row: round(row.mean()) if row.isna().sum() < round(len(pedsql_mapped.columns)/2) else np.nan, axis=1)
    pedsql['psychosocial'] = psychosocial.apply(lambda row: round(row.mean()) if row.isna().sum() < round(len(psychosocial.columns)/2) else np.nan, axis=1)

    pedsql['physical'] = pedsql_mapped[[item for item in q_physical]].apply(lambda row: round(row.mean()) if row.isna().sum() < round(len(q_physical)/2) else np.nan, axis=1)
    pedsql['emotion'] = pedsql_mapped[[item for item in q_emotion]].apply(lambda row: round(row.mean()) if row.isna().sum() < round(len(q_emotion)/2) else np.nan, axis=1)
    pedsql['relation'] = pedsql_mapped[[item for item in q_relation]].apply(lambda row: round(row.mean()) if row.isna().sum() < round(len(q_relation)/2) else np.nan, axis=1)
    pedsql['school'] = pedsql_mapped[[item for item in q_school]].apply(lambda row: round(row.mean()) if row.isna().sum() < round(len(q_school)/2) else np.nan, axis=1)


    pedsql.to_excel(f'Documents/pedsql_{sub}_rated.xlsx',header=True, index=True)
else:
    print(f'Le fichier n\'existe pas')
