import sqlite3
from typing import Callable, TypeVar
from functools import wraps


T = TypeVar('T', str, any)
R = TypeVar('R')


class Query_Db:
    def __init__(self, db_name: str) -> None:
        """Initialize sqlite3 database by passing the name of the db you want to query.
           It creates the databse if it does not exist

        Args:
            db_name (str): The database name
        """
        self.__db_name = db_name
        self.__conn = sqlite3.connect(self.__db_name)

    def conn_manager(fn: Callable[[T], R]) -> Callable[[T], R]:
        """Decorator function to execute sql queries and handle errors

        Args:
            fn (Callable[[T], R]): The function with the query arguments

        Returns:
            Callable[[T], R]: Returns theresult of calling the inner function
        """
        @wraps(fn)
        def inner(*args: T, **kwargs: T) -> R:
            """Gets the query parameters from the passed function and execute sqlite3 execute or executemany depending on the function passed

            Returns:
                R: Returns the sqlite# Row object or None if the cursor has no return
            """
            sql_params = fn(*args, **kwargs)
            conn = args[0].__conn
            cur = conn.cursor()
            try:
                if fn.__name__ == 'query_many':
                    cur.executemany(*sql_params)
                else:
                    cur.execute(*sql_params)
                conn.commit()
                sql_data = cur.fetchall()
                conn.close()
                return sql_data
            except sqlite3.Error as e:
                err_name = e.__class__.__name__
                print(f"{err_name}: {e}")
        return inner

    @conn_manager
    def query(self, query_cmd: str, query_input: tuple = None) -> tuple:
        """Extracts and process the query commmand and inputs to be executed by the connection manager.
            This method calls the sqlite3 execute method from the connection manager
        Args:
            query_cmd (str): The sql query command
            query_input ([type], optional): The parameters to be passed to the query. Defaults to None:any.

        Returns:
            tuple: The arguments to be passed to the sqlite execute command
        """
        if query_input:
            return (query_cmd, query_input)
        return (query_cmd,)

    @conn_manager
    def query_many(self, query_cmd: str, query_input: any = None) -> tuple:
        """Extracts and process the query commmand and inputs to be executed by the connection manager.
            This method calls the sqlite3 executemany method from the connection manager
        Args:
            query_cmd (str): The sql query command
            query_input ([type], optional): The parameters to be passed to the query. Defaults to None:any.

        Returns:
            tuple: The arguments to be passed to the sqlite execute command
        """
        if query_input:
            return (query_cmd, query_input)
        return (query_cmd,)
