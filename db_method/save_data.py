from .db_config import Query_Db

class Save_Scraped_Data:

    def __init__(self, db_name) -> None:
        self.__db_name = db_name

    @property
    def conn(self) -> Query_Db:
        """Returns a conn instance to query sqlite3 databse

        Returns:
            Query_DB: A class containing methods to query and manage sqlite database transactions
        """
        db_name = self.__db_name
        return Query_Db(db_name)

    def create_tables(self, query: str) -> None:
        """A method called to create a table in the database

        Args:
            query (str): The query string
        """
        db = self.conn
        db.query(query)

    def create_quote_table(self):
        """Creates quote table"""
        quote_table = """CREATE TABLE IF NOT EXISTS quotes
        (
            quote TEXT UNIQUE NOT NULL,
            author TEXT NOT NULL
        )
        """
        self.create_tables(quote_table)

    def create_author_table(self):
        """Creates author table"""
        author_table = """CREATE TABLE IF NOT EXISTS authors
        (
            author TEXT UNIQUE NOT NULL,
            date_of_birth TEXT NOT NULL,
            place_of_birth TEXT NOT NULL
        )
        """
        self.create_tables(author_table)

    def insert_data(self, query: str, data: list|tuple):   
        """Inserts data in a table
        data: The datas to inserts
        """ 
        db = self.conn
        db.query_many(query, data)