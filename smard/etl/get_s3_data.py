import os
import boto3
import pandas as pd
from smard.params import *

def get_s3_data(filename):

    s3_session = boto3.Session(profile_name="pyconnector")
    s3_client = s3_session.client("s3")
    df = pd.read_csv(s3_client.get_object(Bucket=BUCKET, Key=filename).get('Body'), parse_dates=['Datetime'])
    return df
