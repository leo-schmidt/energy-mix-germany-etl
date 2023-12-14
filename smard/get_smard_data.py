import requests
import pandas as pd
from convert_timestamp import convert_timestamp_to_date

# create dictionary of filters as defined on https://smard.api.bund.dev/
# each filter corresponds to one possible parameter
filters_dict = {1223: 'Production: Brown coal',
            1224: 'Production: Nuclear',
            1225: 'Production: Wind Offshore',
            1226: 'Production: Hydropower',
            1227: 'Production: Other conventionals',
            1228: 'Production: Other renewables',
            4066: 'Production: Biomass',
            4067: 'Production: Wind Onshore',
            4068: 'Production: Solar',
            4069: 'Production: Hard coal',
            4070: 'Production: Pumped storage',
            4071: 'Production: Natural gas',
            410: 'Consumption: Total (Grid load)',
            4359: 'Consumption: Residual',
            4387: 'Consumption: Pumped storage',
            4169: 'Market price: Germany/Luxembourg'}


def get_latest_timestamp(region="DE",
                         resolution="quarterhour",
                         filter=1223):

    url = f"https://www.smard.de/app/chart_data/{filter}/{region}/index_{resolution}.json"

    response = requests.get(url)
    timestamps = response.json()

    latest_timestamp = timestamps['timestamps'][-1]

    return latest_timestamp

def get_timeseries(region="DE",
                         resolution="quarterhour",
                         filters=filters_dict.keys(),
                         timestamp=1702249200000):

    # instantiate df to hold timeseries data
    timeseries_df = pd.DataFrame()

    # loop over list of filters and pass it to the API request
    for filter in filters:
        url = f"https://www.smard.de/app/chart_data/{filter}/{region}/{filter}_{region}_{resolution}_{timestamp}.json"

        response = requests.get(url)

        timeseries_data = response.json()

        # create dataframe from timeseries data
        filter_df = pd.DataFrame(timeseries_data['series'], columns=['Datetime', filters_dict[filter]])
        filter_df.dropna(inplace=True)

        # only for the first one, replace timeseries_df
        if timeseries_df.empty:
            timeseries_df = filter_df
        # for all other filters, concatenate the
        else:
            timeseries_df = timeseries_df.merge(filter_df)

    # convert UNIX timestamp to date
    timeseries_df['Datetime'] = timeseries_df['Datetime'].apply(convert_timestamp_to_date)

    return timeseries_df
