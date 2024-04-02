import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def _open_sql_connection():
    host = os.environ.get("HOST")
    port = int(os.environ.get("PORT"))
    database = os.environ.get("DATABASE")
    user = os.environ.get("USERNAME")
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
    cursor.execute("INSERT INTO tournoi (nom, lieu, nb_equipe, date_de_debut, date_de_fin) VALUES (%s, %s, %s, %s, %s)",
                   (name, location, team_count, start_date, end_date))
    tournoi_id = connection.insert_id()  # This retrieves the auto-increment ID of the last inserted row
    connection.commit()
    connection.close()
    return tournoi_id


def select_tournaments():
    connection, cursor = _open_sql_connection()
    cursor.execute("SELECT tournoi_id, nom, lieu, nb_equipe, date_de_debut, date_de_fin FROM tournoi")
    tournaments = cursor.fetchall()
    connection.close()
    return tournaments


def select_teams():
    connection, cursor = _open_sql_connection()
    query = """
    SELECT 
        E.equipe_id, E.nom AS equipe_nom, E.pays, E.entraineur_principal, E.stade_domicile,
        J.joueur_id, J.nom AS joueur_nom, J.age, J.position
    FROM 
        Equipe E
    LEFT JOIN 
        Joueur J ON E.equipe_id = J.equipe_id
    ORDER BY
        E.equipe_id, J.joueur_id;
    """
    cursor.execute(query)
    teams = cursor.fetchall()
    connection.close()
    return teams


def delete_tournament(tournament_id):
    connection, cursor = _open_sql_connection()
    cursor.execute("DELETE FROM tournoi WHERE tournoi_id = %s", (tournament_id,))
    connection.commit()  # Make sure to commit the transaction
    connection.close()


if __name__ == '__main__':
    select_tournaments()
