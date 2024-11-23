from dagster import Definitions, load_assets_from_modules, EnvVar
from dagster_azure.adls2 import ADLS2Resource, ADLS2DefaultAzureCredential
from dagster_dbt import DbtCliResource, DbtProject
from pathlib import Path

from energy_mix import params
from energy_mix.resources import PostgresResource

from . import assets  # noqa: TID252


dbt_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "dbt").resolve(),
    # packaged_project_dir=Path(__file__).joinpath("dbt-project").resolve(),
)
dbt_project.prepare_if_dev()

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
        "dbt": DbtCliResource(project_dir=dbt_project),
    },
)
