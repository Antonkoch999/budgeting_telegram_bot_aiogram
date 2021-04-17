"""Create db."""

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file.

    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error:
        print(Error)

    return conn


def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement.

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error:
        print(Error)


def main():
    """Create table in db."""
    database = 'telebot/telebot.db'

    sql_create_budgeting_table = """CREATE TABLE IF NOT EXISTS budgeting (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        category text,
                                        amount real,
                                        income_expense text,
                                        create_at datetime default CURRENT_TIMESTAMP                                        
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create budgeting table
        create_table(conn, sql_create_budgeting_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
