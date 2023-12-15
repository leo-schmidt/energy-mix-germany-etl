from smard.etl.get_smard_data import *
import pandas as pd

def save_to_aws(df:pd.DataFrame,
                filename,
                bucket):
    path = f"{filename}.csv"
    df.to_csv(path, index=False)
