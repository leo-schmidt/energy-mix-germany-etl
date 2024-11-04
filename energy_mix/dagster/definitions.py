from dagster import Definitions, load_assets_from_modules, EnvVar
from dagster_azure.adls2 import ADLS2Resource, ADLS2DefaultAzureCredential

from energy_mix import params
from energy_mix.dagster.resources import PostgresResource

from . import assets  # noqa: TID252

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "adls2": ADLS2Resource(
            storage_account=params.STORAGE_ACCOUNT,
            credential=ADLS2DefaultAzureCredential(kwargs={}),
        ),
        "db": PostgresResource(
            user=EnvVar("PGUSER"),
            password=EnvVar("PGPASSWORD"),
            host=EnvVar("PGHOST"),
            database=EnvVar("PGDATABASE"),
        ),
    },
)
