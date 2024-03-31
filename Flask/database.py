import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def _open_sql_connection():
    host = os.environ.get("HOST")
    port = int(os.environ.get("PORT"))
    database = os.environ.get("DATABASE")
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")

    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=database,
        autocommit=True
    )

    cursor = connection.cursor()
    return connection, cursor


def insert_tournaments(name, location, team_count, start_date, end_date):
    connection, cursor = _open_sql_connection()
    cursor.execute("INSERT INTO tournoi (nom, lieu, nb_equipe, date_de_debut, date_de_fin) "
                   "VALUES (%s, %s, %s, %s, %s)",
                   (name, location, team_count, start_date, end_date))
    connection.close()


def select_tournaments():
    connection, cursor = _open_sql_connection()
    cursor.execute("SELECT nom, lieu, nb_equipe, date_de_debut, date_de_fin FROM tournoi")
    tournaments = cursor.fetchall()
    connection.close()
    return tournaments



if __name__ == '__main__':
    select_tournaments()
