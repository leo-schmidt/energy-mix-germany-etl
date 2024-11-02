import requests
import pandas as pd
from energy_mix_germany.utils.convert_timestamp import convert_timestamp_to_date


class SmardAPIConnector:
    def __init__(self):
        self.base_url = "https://www.smard.de/app/chart_data"

        # create dictionary of filters as defined on https://smard.api.bund.dev/
        # each filter corresponds to one possible parameter
        self.filters_dict = {
            1223: "Production: Brown coal",
            1224: "Production: Nuclear",
            1225: "Production: Wind Offshore",
            1226: "Production: Hydropower",
            1227: "Production: Other conventionals",
            1228: "Production: Other renewables",
            4066: "Production: Biomass",
            4067: "Production: Wind Onshore",
            4068: "Production: Photovoltaics",
            4069: "Production: Hard coal",
            4070: "Production: Pumped storage",
            4071: "Production: Natural gas",
            410: "Consumption: Total (Grid load)",
            4359: "Consumption: Residual",
            4387: "Consumption: Pumped storage",
            4169: "Market price: Germany/Luxembourg",
            3791: "Production forecast: Offshore",
            123: "Production forecast: Onshore",
            126: "Production forecast: Photovoltaics",
            715: "Production forecast: Other",
            5097: "Production forecast: Wind and Photovoltaics",
            122: "Production forecast: Total",
        }

    def get_timestamps(
        self,
        filter: int,
        region: str = "DE",
        resolution: str = "hour",
    ):

        url = f"{self.base_url}/{filter}/{region}/index_{resolution}.json"

        response = requests.get(url)
        timestamps = response.json()

        return timestamps["timestamps"]

    def get_timeseries_df(
        self,
        timestamp: int,
        filter: int,
        region: str = "DE",
        resolution: str = "hour",
    ):
        url = f"{self.base_url}/{filter}/{region}/{filter}_{region}_{resolution}_{timestamp}.json"

        response = requests.get(url)
        if not response.ok:
            return
        ts_json = response.json().get("series")

        ts_df = pd.DataFrame(ts_json, columns=["Datetime", self.filters_dict[filter]])
        ts_df["Datetime"] = ts_df["Datetime"].apply(convert_timestamp_to_date)
        return ts_df.dropna()
