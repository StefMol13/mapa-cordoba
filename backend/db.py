import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=192.168.0.108;"
        "DATABASE=pentaho;"
        "UID=powerbi;"
        "PWD=34salud56;"
    )
