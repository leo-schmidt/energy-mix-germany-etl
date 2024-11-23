{{ config(materialized='incremental') }}
select
  "Datetime" as "datetime",
  market_price_germany_luxembourg,
  consumption_total,
  production_forecast_offshore as production_forecast_wind_offshore,
  production_forecast_onshore as production_forecast_wind_onshore,
  production_forecast_other,
  production_forecast_photovoltaics,
  production_forecast_wind_and_photovoltaics,
  production_forecast_total,
  production_wind_offshore,
  production_wind_onshore,
  ( production_hard_coal
  + production_hydropower
  + production_natural_gas
  + production_other_conventionals
  ) as production_conventionals,
  ( production_biomass
  + production_other_renewables
  + production_pumped_storage
  ) as production_other_renewables,
  production_photovoltaics,
  ( production_photovoltaics
  + production_wind_onshore
  + production_wind_offshore
  ) as production_wind_and_photovoltaics,
  ( production_biomass
  + production_hard_coal
  + production_hydropower
  + production_natural_gas
  + production_other_conventionals
  + production_other_renewables
  + production_photovoltaics
  + production_pumped_storage
  + production_wind_onshore
  + production_wind_offshore
  ) as production_total
from raw
{% if is_incremental() %}

where "Datetime" > (select coalesce(max("datetime"),'1900-01-01 00:00:00.000') from {{ this }} )

{% endif %}
