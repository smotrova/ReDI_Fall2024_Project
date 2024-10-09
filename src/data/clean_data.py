import pandas as pd
import numpy as np

def mainbranch_cleaned(df):
    
    map_dict = { 
        'I am a developer by profession':'Developer',
        'I am not primarily a developer, but I write code sometimes as part of my work/studies':'Coder',
        'I code primarily as a hobby':'Amateur',
        'I am learning to code':'Learner',
        'I used to be a developer by profession, but no longer am':'Ex-Developer',
        'None of these':'Other'
    }
    
    if 'MainBranch' in df.columns:
        MainBranch = df.MainBranch.map(map_dict, na_action='ignore')
        return MainBranch
    else:
        return pd.Series(index=df.index, name="Mainbranch")

def age_cleaned(df):
      
    if 'Age' in df.columns:
        Age = df.Age.apply(lambda x: np.nan if x=='Prefer not to say' else x)
        return Age
    else:
        return pd.Series(index=df.index, name="Age")

def employment_cleaned(df):
    
    if 'Employment' in df.columns:
        fltr = df.Employment.str.split(';', expand=False).apply(lambda x: 0 if x!=x  else len(x))==1
        df.loc[~fltr, 'Employment'] = np.nan
        Employment = df.Employment.apply(lambda x: np.nan if x=='I prefer not to say' else x)
        return Employment        
    else:
        return pd.Series(index=df.index, name="Employment")

def country_cleaned(df):
    
    if 'Country' in df.columns:
        Country = df.Country.apply(lambda x: 'Vietnam' if x=='Viet Nam' else x)
        return Country        
    else:
        return pd.Series(index=df.index, name="Country")

def edlevel_cleaned(df):
    
    if 'EdLevel' in df.columns:
        EdLevel = df.EdLevel
        return EdLevel
    else:
        return pd.Series(index=df.index)

def age_yearscode_cleaned(df):
    
    if 'Age' in df.columns and 'YearsCodePro' in df.columns and 'YearsCode' in df.columns:
        
        Age = df["Age"].apply(lambda x: np.nan if x=='Prefer not to say' else x)

        experience_pro = df.YearsCodePro.apply(lambda x: '0' if x=='Less than 1 year' else x) \
                        .apply(lambda x: '51' if x=='More than 50 years' else x) \
                        .apply(lambda x: int(x) if x==x else x)

        experience_tot = df.YearsCode.apply(lambda x: '0' if x=='Less than 1 year' else x) \
                        .apply(lambda x: '51' if x=='More than 50 years' else x) \
                        .apply(lambda x: int(x) if x==x else x)

        YearsCodePro = experience_pro
        YearsCodePro.loc[experience_tot-experience_pro < 0] = np.nan

        YearsCode = experience_tot
        YearsCode.loc[experience_tot-experience_pro < 0] = np.nan
        
        Age_boundaries = {
            '18-24 years old':(18,24), 
            '25-34 years old':(25,34), 
            '45-54 years old':(45,54),
            '35-44 years old':(35,44), 
            'Under 18 years old':(13, 17), 
            '55-64 years old': (55, 64),
            '65 years or older': (65, 90)
        }

        CodeInterval = df["Age"].map(Age_boundaries).apply(lambda x: (x[0]-6, x[1]-6) if x==x else x)

        tmp = pd.concat([Age, YearsCode, YearsCodePro, CodeInterval], 
                        keys=["Age", "YearsCode", "YearsCodePro", "CodeInterval"],  axis=1)

        fltr = tmp.apply(lambda x: x[1]<x[3][1] if x[3]==x[3] and x[1]==x[1] else False,  axis=1)

        tmp.loc[~fltr, :] = np.nan
        
        return tmp.loc[:, ["Age", "YearsCode", "YearsCodePro"]]
        
    else:
        return pd.DataFrame(index=df.index, columns = ["Age", "YearsCode", "YearsCodePro"])

def workexp_cleaned(df):
    
    Age = age_yearscode_cleaned(df)["Age"]
    
    if 'WorkExp' in df.columns:
                
        Age_boundaries = {
            '18-24 years old':(18,24), 
            '25-34 years old':(25,34), 
            '45-54 years old':(45,54),
            '35-44 years old':(35,44), 
            'Under 18 years old':(13, 17), 
            '55-64 years old': (55, 64),
            '65 years or older': (65, 90)
        }

        AgeInterval = Age.map(Age_boundaries).apply(lambda x: (x[0], x[1]) if x==x else x)

        tmp = pd.concat([Age, df.WorkExp, AgeInterval ], 
                        keys=["Age", "WorkExp", "AgeInterval"],  axis=1)

        fltr = tmp.apply(lambda x: x[1]<x[2][0] if x[1]==x[1] and x[2]==x[2] else False,  axis=1)

        tmp.loc[~fltr, "WorkExp"] = np.nan
        
        return tmp.loc[:, ["WorkExp"]]
        
    else:
        return pd.DataFrame(index=df.index, columns = ["WorkExp"])

def dataset_cleaned(df):
    
    MainBranch = mainbranch_cleaned(df)
    AgeYearsCode = age_yearscode_cleaned(df)
    Age = AgeYearsCode["Age"]
    Employment = employment_cleaned(df)
    RemoteWork = df["RemoteWork"]
    EdLevel = edlevel_cleaned(df)
    YearsCode = AgeYearsCode["YearsCode"]
    YearsCodePro = AgeYearsCode["YearsCodePro"]
    LanguageHaveWorkedWith = df["LanguageHaveWorkedWith"]
    DevType = df["DevType"]
    Country = country_cleaned(df)
    ConvertedCompYearly = df["ConvertedCompYearly"]
    ICorPM = df["ICorPM"]
    WorkExp = workexp_cleaned(df)
    Industry = df["Industry"]
    
    df_cleaned = pd.concat([MainBranch, Age, Employment, RemoteWork, EdLevel, YearsCode, YearsCodePro, 
                      LanguageHaveWorkedWith, DevType, Country, ConvertedCompYearly, ICorPM, WorkExp, Industry],
                    axis=1)
    df_cleaned = df_cleaned.drop_duplicates().dropna(subset=["ConvertedCompYearly"])
    
    return df_cleaned


