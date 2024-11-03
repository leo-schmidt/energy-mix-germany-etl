from datetime import datetime
from io import BytesIO
from dagster import AssetExecutionContext, WeeklyPartitionsDefinition, asset
from dagster_azure.adls2 import ADLS2Resource
import pandas as pd
from energy_mix import params
from energy_mix.smard_api.smard_api_connector import SmardAPIConnector
from energy_mix.utils.adls2_file_handler import ADLS2FileHandler
from energy_mix.utils.convert_timestamp import convert_date_to_timestamp


weekly_partition = WeeklyPartitionsDefinition(
    start_date="2014-12-29",  # start of smard data
    day_offset=1,  # week starts on monday
    # end_offset=1,
    fmt="%Y-%m-%d",
)


@asset(partitions_def=weekly_partition)
def energy_mix_raw_data(context: AssetExecutionContext, adls2: ADLS2Resource):
    smard = SmardAPIConnector()
    file_handler = ADLS2FileHandler(adls2)

    ts_unix = convert_date_to_timestamp(
        context.partition_key,
        dt_format="%Y-%m-%d",
    )

    for filter_key, filter_name in smard.filters_dict.items():

        ts_df = smard.get_timeseries_df(
            ts_unix, filter_key, params.REGION, params.RESOLUTION
        )

        if not isinstance(ts_df, pd.DataFrame):
            continue

        file_handler.upload_df_as_timestamped_parquet(
            df=ts_df,
            file_system=params.CONTAINER,
            directory=params.RAW_PATH,
            timestamp=context.partition_key,
            file_name=filter_name,
        )


@asset(partitions_def=weekly_partition)
def energy_mix_merged_data(context: AssetExecutionContext, adls2: ADLS2Resource):
    fs_client = adls2.adls2_client.get_file_system_client(file_system=params.CONTAINER)
    ts_dt = datetime.strptime(context.partition_key, "%Y-%m-%d")

    merged_df = pd.DataFrame()

    paths = fs_client.get_paths(path=f"{params.RAW_PATH}/{ts_dt.year}/{ts_dt.month}")
    for path in paths:
        # filter for correct partition
        if context.partition_key not in path.name:
            continue
        # download file
        file_client = fs_client.get_file_client(path)
        download = file_client.download_file().readall()
        download_bytes = BytesIO(download)
        if path.name.endswith(".parquet"):
            df = pd.read_parquet(download_bytes)
        elif path.name.endswith(".csv"):
            df = pd.read_csv(download_bytes)
        else:
            continue

        # merge into dataframe with all columns
        if merged_df.empty:
            merged_df = df
        else:
            merged_df = merged_df.merge(df, on="Datetime")

    # upload to data lake
    file_handler = ADLS2FileHandler(adls2)
    file_handler.upload_df_as_timestamped_parquet(
        df=merged_df,
        file_system=params.CONTAINER,
        directory=params.MERGED_PATH,
        timestamp=context.partition_key,
        file_name="merged",
    )
