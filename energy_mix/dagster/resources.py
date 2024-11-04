from dagster import ConfigurableResource
from sqlalchemy import Engine, create_engine


class PostgresResource(ConfigurableResource):
    user: str
    password: str
    host: str
    database: str

    def create_engine(self) -> Engine:
        conn_string = (
            f"postgresql://{self.user}:{self.password}@{self.host}/{self.database}"
        )
        return create_engine(conn_string)
