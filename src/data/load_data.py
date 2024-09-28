import pandas as pd
import zipfile, requests
from io import BytesIO  

def get_data(url, needed_file_name):
   
    data = requests.get(url)
    zfile = zipfile.ZipFile(BytesIO(data.content)) 
    filenames = zfile.namelist()

    df = pd.DataFrame()
                                 
    for name in filenames:
        if name == needed_file_name:                       
            needed_file = zfile.open(name, "r")
            df = pd.read_csv(needed_file)
            zfile.close()
            return df 
    raise Exception ('File not found '+ needed_file_name)
