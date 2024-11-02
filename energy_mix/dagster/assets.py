from io import BytesIO
from dagster import asset
from dagster_azure.adls2 import ADLS2Resource
from energy_mix import params
from energy_mix.smard_api.smard_api_connector import SmardAPIConnector
from energy_mix.utils.convert_timestamp import convert_timestamp_to_date

region = params.REGION
resolution = params.RESOLUTION


@asset
def energy_mix_data(adls2: ADLS2Resource):
    smard = SmardAPIConnector()
    filters_dict = smard.filters_dict

    for filter_key, filter_name in filters_dict.items():
        ts_unix = smard.get_timestamps(filter_key, region, resolution)[-1]
        ts_dt = convert_timestamp_to_date(ts_unix)

        ts_df = smard.get_timeseries_df(ts_unix, filter_key, region, resolution)

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
