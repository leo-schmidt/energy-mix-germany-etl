from datetime import datetime
from io import BytesIO
from dagster_azure.adls2 import ADLS2Resource
import pandas as pd


class ADLS2FileHandler:
    def __init__(self, adls2: ADLS2Resource):
        self.adls2 = adls2

    def upload_df_as_timestamped_parquet(
        self,
        df: pd.DataFrame,
        file_system: str,
        directory: str,
        timestamp: str,
        file_name: str,
    ) -> None:
        buffer = BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        directory_client = self.adls2.adls2_client.get_directory_client(
            file_system=file_system,
            directory=directory,
        )
        timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d")
        file_path = f"{timestamp_dt.year}/{timestamp_dt.month}/{timestamp_dt.date()}_{file_name}.parquet"
        file_client = directory_client.get_file_client(file=file_path)
        file_client.upload_data(buffer, overwrite=True)
