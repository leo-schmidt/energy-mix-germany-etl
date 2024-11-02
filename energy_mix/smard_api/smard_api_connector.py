import requests
import pandas as pd
from energy_mix.utils.convert_timestamp import convert_timestamp_to_date


class SmardAPIConnector:
    def __init__(self):
        self.base_url = "https://www.smard.de/app/chart_data"

        # create dictionary of filters as defined on https://smard.api.bund.dev/
        # each filter corresponds to one possible parameter
        self.filters_dict = {
            1223: "production_hard_coal",  # "Production: Brown coal",
            1224: "production_nuclear",  # "Production: Nuclear",
            1225: "production_wind_offshore",  # "Production: Wind Offshore",
            1226: "production_hydropower",  # "Production: Hydropower",
            1227: "production_other_conventionals",  # "Production: Other conventionals",
            1228: "production_other_renewables",  # "Production: Other renewables",
            4066: "production_biomass",  # "Production: Biomass",
            4067: "production_wind_onshore",  # "Production: Wind Onshore",
            4068: "production_photovoltaics",  # "Production: Photovoltaics",
            4069: "production_hard_coal",  # "Production: Hard coal",
            4070: "production_pumped_storage",  # "Production: Pumped storage",
            4071: "production_natural_gas",  # "Production: Natural gas",
            410: "consumption_total",  # "Consumption: Total (Grid load)",
            4359: "consumption_residual",  # "Consumption: Residual",
            4387: "consumption_pumped_storage",  # "Consumption: Pumped storage",
            4169: "market_price_germany_luxembourg",  # "Market price: Germany/Luxembourg",
            3791: "production_forecast_offshore",  # "Production forecast: Offshore",
            123: "production_forecast_onshore",  # "Production forecast: Onshore",
            126: "production_forecast_photovoltaics",  # "Production forecast: Photovoltaics",
            715: "production_forecast_other",  # "Production forecast: Other",
            5097: "production_forecast_wind_and_photovoltaics",  # "Production forecast: Wind and Photovoltaics",
            122: "production_forecast_total",  # "Production forecast: Total",
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
