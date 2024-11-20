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
    
    country_clean = {
        'Czech Republic' : 'Czechia [Czech Republic]',
        'France' : 'France [French Republic]',
        'Hong Kong (S.A.R.)' : 'China, Hong Kong Special Administrative Region',
        'Republic of Korea' : 'Republic of Korea [South Korea]',
        'South Korea': 'Republic of Korea [South Korea]',
        'Turkey':'Türkiye',
        }
        
    # {
    #     'Viet Nam':'Vietnam',
    #     'United Kingdom of Great Britain and Northern Ireland':'UK',
    #     'United States of America':'USA'
    # }

    if 'Country' in df.columns:
        Country = df.Country.apply(lambda x: country_clean[x] if x in country_clean.keys() else x)
        return Country        
    else:
        return pd.Series(index=df.index, name="Country")
    
def region(ser):

    regions = pd.read_html('https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_the_United_Nations_geoscheme')
    country_region = regions[0].set_index('Country or Area')['Geographical subregion'].to_dict()

    Region =  ser.apply(lambda x: country_region[x] if x in country_region.keys() else None).rename('Region', inplace=True)
    
    return Region   

def edlevel_cleaned(df):

    # education_level = { 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)' : 'Graduated',
    # 'Some college/university study without earning a degree':'Non-graduated',
    # 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':'Graduated',
    # 'Primary/elementary school':'Non-graduated',
    # 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':'Graduated',
    # 'Associate degree (A.A., A.S., etc.)':'Non-graduated',
    # 'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)':'Non-graduated',
    # 'Something else':np.nan 
    # }

    education_level = { 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)' : 'Bachelor',
    'Some college/university study without earning a degree':'Non-graduated',
    'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':'Master',
    'Primary/elementary school':'Non-graduated',
    'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':'PhD',
    'Associate degree (A.A., A.S., etc.)':'Non-graduated',
    'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)':'Non-graduated',
    'Something else':np.nan 
    }
    
    if 'EdLevel' in df.columns:
        EdLevel = df.EdLevel.map(education_level)
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

def devtype_cleaned(df):

    if 'DevType' in df.columns:
        DevType = df['DevType'].apply(lambda x: np.nan if x == 'Other (please specify):' else x)
        return DevType
    else:
        return pd.DataFrame(index=df.index, columns = ["DevType"])

def dataset_cleaned(df):
    
    MainBranch = mainbranch_cleaned(df)
    AgeYearsCode = age_yearscode_cleaned(df)
    Age = AgeYearsCode["Age"]
    Employment = employment_cleaned(df)
    RemoteWork = df["RemoteWork"]
    EdLevel = df.EdLevel
    YearsCode = AgeYearsCode["YearsCode"]
    YearsCodePro = AgeYearsCode["YearsCodePro"]
    LanguageHaveWorkedWith = df["LanguageHaveWorkedWith"]
    DevType = devtype_cleaned(df)
    Country = country_cleaned(df)
    ConvertedCompYearly = df["ConvertedCompYearly"]
    ICorPM = df["ICorPM"]
    WorkExp = workexp_cleaned(df)
    Industry = df["Industry"]
    
    df_cleaned = pd.concat([MainBranch, Age, Employment, RemoteWork, EdLevel, YearsCode, YearsCodePro, 
                      LanguageHaveWorkedWith, DevType, Country, ConvertedCompYearly, ICorPM, WorkExp, Industry],
                    axis=1)
    df_cleaned = df_cleaned.drop_duplicates().dropna(subset=["ConvertedCompYearly"])
    
    # delete records where `Employment` status "Retired" only and `CompYeraly` is indicated
    fltr_retired = df_cleaned.Employment == "Retired"
    df_cleaned = df_cleaned.loc[~fltr_retired]
    
    # delete records where `Employment` status is "Employed, full-time" 
    # and current job, the one person does most of the time, is "Student"
    fltr_student_fullTimeEmpl = (df_cleaned.DevType=="Student") & (df_cleaned.Employment=="Employed, full-time")
    df_cleaned = df_cleaned.loc[~fltr_student_fullTimeEmpl]
    
    df_cleaned.reset_index(inplace=True, drop=True)
    
    return df_cleaned

def dataset_cleaned1(df):
        
    AgeYearsCode = age_yearscode_cleaned(df)
    EdLevel = edlevel_cleaned(df)
    YearsCodePro = AgeYearsCode["YearsCodePro"]
    LanguageHaveWorkedWith = df["LanguageHaveWorkedWith"]
    DevType = devtype_cleaned(df)
    Country = country_cleaned(df)
    Region = region(Country)
    ConvertedCompYearly = df["ConvertedCompYearly"]
    ICorPM = df["ICorPM"]
    WorkExp = workexp_cleaned(df)
    Industry = df["Industry"]

    # add a new feature number of programming languages

    NLanguageHaveWorkedWith = df.LanguageHaveWorkedWith.str.split(";").apply(lambda x: len(x) if x==x else np.nan).rename("NLanguageHaveWorkedWith")
    
    df_cleaned = pd.concat([EdLevel, YearsCodePro, LanguageHaveWorkedWith, NLanguageHaveWorkedWith,
                             DevType, Country, Region, ConvertedCompYearly, ICorPM, WorkExp, Industry],
                    axis=1)
    
    df_cleaned = df_cleaned.drop_duplicates().dropna() #dropna(subset=["ConvertedCompYearly"])
    df_cleaned.reset_index(inplace=True, drop=True)
    
    return df_cleaned