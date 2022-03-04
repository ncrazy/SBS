from datetime import date, datetime
import sqlite3
from sqlite3 import Error


def Create_Connection(Dbfile):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    Conn = None
    try:
        Conn = sqlite3.connect(Dbfile)
    except Error as e:
        print(e)

    return Conn

def Create_Table(Conn, Create_Table_Sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = Conn.cursor()
        c.execute(Create_Table_Sql)
    except Error as e:
        print(e)


def Insert_GpsData(Conn, GpsData):
    """
    Insert new GpsData into the GpsData table
    :param Conn:
    :param GpsData:
    :return: project id
    """
    Sql = ''' INSERT INTO GpsData(GpsDateTime,Lat,Long,Speed)
              VALUES(?,?,?,?) '''
    Cur = Conn.cursor()
    Cur.execute(Sql, GpsData)
    Conn.commit()
    return Cur.lastrowid



def main():
    Database = r".\db\sensornodedb.db"

    sql_create_GpsData_table = """ CREATE TABLE IF NOT EXISTS GpsData (
                                        GpsDateTime text PRIMARY KEY,
                                        Lat real NOT NULL,
                                        Long real NOT NULL,
                                        Speed real
                                    ); """

    # create a database connection
    Conn = Create_Connection(Database)
    with Conn:
        # create GpsData table
        Create_Table(Conn,sql_create_GpsData_table)
        # insert GPS data
        GpsData = (str(datetime.now()), 100.001, 102.002,24.2)
        Insert_GpsData(Conn, GpsData)

        


if __name__ == '__main__':
    main()