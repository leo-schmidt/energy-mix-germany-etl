{{ config(materialized='incremental') }}
select
  datetime,
  market_price_germany_luxembourg,
  consumption_total,
  production_forecast_other as production_forecast_conventionals,
  production_forecast_wind_and_photovoltaics as production_forecast_renewables,
  production_forecast_total,
  round((production_forecast_wind_and_photovoltaics / production_forecast_total)::numeric, 4) as production_forecast_renewables_proportion,
  round((production_forecast_other / production_forecast_total)::numeric, 4) as production_forecast_conventionals_proportion,
  production_conventionals,
  round((production_wind_and_photovoltaics + production_other_renewables)::numeric, 4) as production_renewables,
  production_total,
  round((( production_wind_and_photovoltaics + production_other_renewables) / production_total)::numeric, 4) as production_renewables_proportion,
  round((production_conventionals / production_total)::numeric, 4) as production_conventionals_proportion
from {{ ref('staging') }}
{% if is_incremental() %}

where "datetime" > (select coalesce(max("datetime"),'1900-01-01 00:00:00.000') from {{ this }} )

{% endif %}
