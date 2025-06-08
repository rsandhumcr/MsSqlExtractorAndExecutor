import pyodbc
from sqlalchemy.engine import URL

connection_config = {
    'local' : {
        'db_name': 'AdventureWorksLT2019',
        'connection_str' : f'mssql+pyodbc://./AdventureWorksLT2019?driver=ODBC+Driver+17+for+SQL+Server',
    },
    'local2': {
        'db_name': 'AdventureWorksLT2019',
        'connection_str': f'mssql+pyodbc://user02:user02@./AdventureWorksLT2019?driver=ODBC+Driver+17+for+SQL+Server',
    },
    'AdventureWorksLT2019_v01' : {
        'db_name': 'AdventureWorksLT2019',
        'connection_str' : URL.create(
            "mssql+pyodbc",
            username="user02",
            password="user02",
            host=".",
            database="AdventureWorksLT2019",
            query={
                "driver": "SQL Server",
            }),
    },
    'AdventureWorksLT2019_v02': {
        'db_name': 'AdventureWorksLT2019',
        'connection_str': URL.create(
            "mssql+pyodbc",
            username="user02",
            password="user02",
            host="127.0.0.1",
            port=1433,
            database="AdventureWorksLT2019",
            query={
                "driver": "ODBC Driver 17 for SQL Server",
                "Encrypt": "yes",
                "TrustServerCertificate": "yes",
            }),
    }
}

class DatabaseConfig:

    @staticmethod
    def get_connection_config_names() -> list[str]:
        return list(connection_config.keys())

    @staticmethod
    def get_connection(config_name:str) -> dict[str, str | URL]:
        return connection_config[config_name]

    @staticmethod
    def get_all_installed_drivers():
        print('Installed Drivers pyodbc can use:')  # this will list down all the drivers available in your local P
        print("\n".join(pyodbc.drivers()))
