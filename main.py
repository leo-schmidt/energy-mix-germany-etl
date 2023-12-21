from smard.etl.get_smard_data import *
from smard.etl.save_to_aws import *
from datetime import datetime

ts = get_latest_timestamp()

df = get_timeseries(timestamp=ts)
save_to_aws(df, 'test_data', "")
