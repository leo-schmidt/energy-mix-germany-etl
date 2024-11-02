from datetime import datetime
from io import BytesIO
from dagster import AssetExecutionContext, WeeklyPartitionsDefinition, asset
from dagster_azure.adls2 import ADLS2Resource
import pandas as pd
from energy_mix import params
from energy_mix.smard_api.smard_api_connector import SmardAPIConnector
from energy_mix.utils.convert_timestamp import convert_date_to_timestamp

region = params.REGION
resolution = params.RESOLUTION


@asset(
    partitions_def=WeeklyPartitionsDefinition(
        start_date="2014-12-29",  # start of smard data
        day_offset=1,  # week starts on monday
        # end_offset=1,
    )
)
def energy_mix_data(context: AssetExecutionContext, adls2: ADLS2Resource):
    smard = SmardAPIConnector()

    ts_dt = datetime.strptime(context.partition_key, "%Y-%m-%d")
    ts_unix = convert_date_to_timestamp(
        context.partition_key,
        dt_format="%Y-%m-%d",
    )

    for filter_key, filter_name in smard.filters_dict.items():

        ts_df = smard.get_timeseries_df(ts_unix, filter_key, region, resolution)

        if not isinstance(ts_df, pd.DataFrame):
            continue

        buffer = BytesIO()
        ts_df.to_csv(buffer, index=False)
        buffer.seek(0)

        directory_client = adls2.adls2_client.get_directory_client(
            file_system="energymix",
            directory="ts-data",
        )
        file_path = f"{ts_dt.year}/{ts_dt.month}/{ts_dt.date()}_{filter_name}.csv"
        file_client = directory_client.get_file_client(file=file_path)
        file_client.upload_data(buffer, overwrite=True)
