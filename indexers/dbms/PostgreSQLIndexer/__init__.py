__copyright__ = "Copyright (c) 2021 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import pickle
from typing import Optional

from jina.executors.indexers import BaseIndexer


class PostgreSQLDBMSIndexer(BaseIndexer):
    # TODO:  this class need to be a subclass from the DBMSIndexer (when it's merged into master)
    """:class:`PostgreSQLDBMSIndexer` PostgreSQL based KV Indexer.
    Initialize the PostgreSQLDBIndexer.

    :param hostname: hostname of the machine
    :param port: the port
    :param username: the username to authenticate
    :param password: the password to authenticate
    :param database: the database name
    :param collection: the collection name
    :param args: other arguments
    :param kwargs: other keyword arguments
    """

    def __init__(
        self,
        hostname: str = "127.0.0.1",
        port: int = 5432,
        username: str = "postgres",
        password: str = "123456",
        database: str = "postgres",
        table: Optional[str] = "default_table",
        *args,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database
        self.table = table
        self.connect()

    def get_connection(self):
        return self.connect()

    def connect(self):
        """Connect to the database. """

        import psycopg2
        from psycopg2 import Error

        try:
            self.connection = psycopg2.connect(
                user=self.username,
                password=self.password,
                database=self.database_name,
                host=self.hostname,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
            self.logger.info("Successfully connected to the database")
            self.create_table()
            self.connection.commit()
        except (Exception, Error) as error:
            self.logger.error("Error while connecting to PostgreSQL", error)
        return self

    def create_table(self):
        """
        Create Table with id, vecs and metas.
        """

        self.cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", (self.table,))
        if self.cursor.fetchone()[0]:
            self.logger.info("Using existing table")
        else:
            try:
                self.cursor.execute(
                    f"""DROP TABLE IF EXISTS {self.table};
                                    CREATE TABLE {self.table} (
                                    ID INT PRIMARY KEY, 
                                    VECS BYTEA, 
                                    METAS BYTEA);"""
                )
                self.logger.info("Successfully table created")
            except:
                self.logger.error("Error while creating table!")

    def add(self, ids, vecs, metas, *args, **kwargs):
        """Insert the documents into the database.

        :param ids: List of doc ids to be added
        :param vecs: List of vecs to be added
        :param metas: List of metas of docs to be added
        :return record: List of Document's id added
        """

        self.cursor.execute(f"DELETE FROM {self.table}")
        for i in range(len(ids)):
            self.cursor.execute(
                f"INSERT INTO {self.table} (ID, VECS, METAS) VALUES (%s, %s, %s)",
                (ids[i], pickle.dumps(vecs), pickle.dumps(metas)),
            )
        self.connection.commit()
        self.cursor.execute(f"SELECT ID from {self.table}")
        record = self.cursor.fetchall()
        return record

    def update(self, id, vecs, metas, *args, **kwargs):
        """Updated document from the database.

        :param ids: Id of Doc to be updated
        :param vecs: List of vecs to be updated
        :param metas: List of metas of docs to be updated
        :return record: List of Document's id after update
        """

        self.cursor.execute(
            f"UPDATE {self.table} SET VECS = %s, METAS = %s WHERE ID = %s",
            (pickle.dumps(vecs), pickle.dumps(metas), id),
        )
        self.connection.commit()
        self.cursor.execute(f"SELECT ID from {self.table}")
        record = self.cursor.fetchall()
        return record

    def delete(self, id, *args, **kwargs):
        """Delete document from the database.

        :param id: Id of Document to be removed
        :return record: List of Document's id after deletion
        """

        self.cursor.execute(f"DELETE FROM {self.table} where (ID) = (%s) ", id)
        self.connection.commit()
        count = self.cursor.rowcount
        self.cursor.execute(f"SELECT ID from {self.table}")
        record = self.cursor.fetchall()
        return record

    def dump(self, uri, shards, formats):
        raise NotImplementedError

    def __exit__(self, *args):
        """ Make sure the connection to the database is closed."""

        from psycopg2 import Error

        try:
            self.connection.close()
            self.cursor.close()
            print("PostgreSQL connection is closed")
        except (Exception, Error) as error:
            print("Error while closing: ", error)
