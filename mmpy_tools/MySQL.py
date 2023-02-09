"""
Custom MySQL connector using os .env parameters (DB_HOST, DB_PASSORD)
To show all details:
```
help(MySQL)
```
"""

import os
import pandas as pd
from sqlalchemy import create_engine

#%% MySQL class
class MySQL:
    """Custom MySQL connector using os .env parameters (DB_HOST, DB_PASSORD)

    Arguments:
        *dbname*: name of the database (optional)  

        *dbhost*: DB host (optional). Will try to use DB_HOST from .env  

        *dbuser*: DB user (optional). Will try to use DB_USER from .env

        *dbpassword*: DB Password (optional). Will try to use DB_PASSWORD from .env  

    Example
    -------
    Get credentials from .env::

        from dotenv import load_dotenv
        load_dotenv()
        credentials = {"DB_HOST":os.environ.get("DB_HOST"),
                       "DB_PASSWORD":os.environ.get("DB_PASSWORD"),
                       "DB_USER":os.environ.get("DB_USER","root")}

    Connect to existing database::

        from chatbot_tools import MySQL
        m = MySQL("logs",credentials["DB_HOST"],credentials["DB_PASSWORD"])
        m.query_table("activity")

    Create new database::

        m = MySQL()
        m.create_db(dbname="test_mysql",drop=False)
        m = MySQL("test_mysql")
        m.create_table("test_table",
                    {"id":"int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY",
                    "service":"varchar(20) NOT NULL"})
        m.insert_table(pd.DataFrame({"id":[1,2],"service":["parts","phrase"]}),
                    "test_table",
                    truncate=True)
        m.execute_sql_file("sql/files_db.sql")
    """
    def __init__(self,
                 dbname: str = "",
                 dbhost: str = "",
                 dbuser: str = "",
                 dbpassword: str = ""):

        # Get password and host from .env if not provided
        if dbhost == "":
            dbhost = os.environ.get("DB_HOST")
        if dbpassword == "":
            dbpassword = os.environ.get("DB_PASSWORD")
        if dbuser == "":
            dbuser = os.environ.get("DB_USER","root")

        self.engine = create_engine(f"mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}")
        self.engine.connect()
        self.dbname = dbname

    def create_db(self, dbname: str = "", drop: bool =True) -> None:
        """Aux function to create the database (=schema in MySQL)

        Arguments:
            *dbname*: name of the database to be created  

            *drop*: if existing db should be dropped (bool)  
        """
        if drop is True:
            try:
                self.engine.execute(f"DROP DATABASE `{dbname}`;")
            except:
                pass
        self.engine.execute(f"CREATE DATABASE `{dbname}`;")

    def create_table(self, table_name: str, table_def: dict, drop: bool = True) -> None:
        """Aux function to create the database table from definition stored in a DataFrame

        Arguments:
            *table_name*: name of the table

            *table_def*: table definition, see example below (dict)

            *drop*: if the table should be dropped

        Example
        -------
        Create a files_db table::

            table_name = "files_db"
            table_def = {"id":"int(11) NOT NULL AUTO_INCREMENT","service":"varchar(20) NOT NULL"}
            self.create_table(table_name,table_def)
        """
        # Remove the table first (if exists)
        if drop is True:
            try:
                self.engine.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
            except:
                pass
        sql = f"CREATE TABLE {table_name} ("
        for tablename, definition in table_def.items():
            sql += f"{tablename} {definition},"
        sql = sql[0:-1] + ");"
        self.engine.execute(sql)

    def execute_sql_file(self, filename: str) -> None:
        """Execute SQL command stored in a formated file

        Arguments:
            *filename*: name of the file

        Example
        -------
        Pass filename for processing::

            filename = "sql/files_db.sql"
            DB.execute_sql_file(filename)

        """
        with open(filename,"r") as fid:
            sql = fid.read()
        for command in sql.split(";"):
            command = command.replace("\n","").replace("\t","")
            if len(command) > 4:
                self.engine.execute(command)

    def query_table(self,table_name: str) -> pd.DataFrame:
        """Query data to dataframe

        Arguments:
            *table_name*: name of the table to be queried

        Returns:
            Queried table as dataframe

        """
        return self.query_sql(f"SELECT * from `{table_name}`")

    def query_sql(self, sql: str) -> pd.DataFrame:
        """Query data to dataframe

        Arguments:
            *sql*: sql command
        """
        return pd.read_sql_query(sql, self.engine)

    def insert_table(self, df: pd.DataFrame, table_name: str, truncate: bool = False) -> None:
        """Insert values from dataframe to given table

        Arguments:
            *df*: dataframe with column names identical with the database

            *table_name*: table for insertion

            *truncate*: if the table should be truncated before insertion

        Example
        -------
        Insert own dataframe::

            import pandas as pd
            df = pd.DataFrame({"id":[0,1],
                            "type":["parts","phrase"],
                            "message":["ahoj","Office Management"]})
            table = "keywords"
            truncate = True

            self.insert_table(df,table,truncate)
        """
        if truncate is True:
            self.engine.execute(f"TRUNCATE TABLE `{table_name}`")

        # pandas.to_sql does not for for some reason. Insert manually
        cols = "(`"+"`,`".join(df.columns)+"`)"
        df = df.replace("'","''",regex=True)
        for i in range(df.shape[0]):
            values = "','".join([f'{i}' for i in df.iloc[i].values])
            query = f"INSERT INTO `{table_name}` {cols} VALUES ('{values}');"
            self.engine.execute(query.replace("'nan'","NULL").replace("'None'","NULL"))

    def delete_id(self, id: str, table: str) -> None:
        """Delete for from a table where ID equals give value

        Arguments:
            *id*: ID to be deleted

            *table*: name of the table

        Example
        -------
        Delete entry where ID column = 10::

            m = MySQL("backend_admin")
            m.delete_id(10,"files")
        ```
        """
        self.delete_where(f"((`id` = '{id}'))",table)

    def delete_where(self, condition: str, table: str) -> None:
        """Delete for from a table where give condition is met

        Arguments:
            *condition*: full where condition

            *table*: name of the table


        Example
        -------
        For: DELETE FROM `files` WHERE `id` = '10';::

            delete_where("`id` = '10'","files")
        ```
        """
        self.engine.execute(f"DELETE FROM `{table}` WHERE {condition}")
