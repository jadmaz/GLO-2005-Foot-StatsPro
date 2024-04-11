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
    connection, cursor = _open_sql_connection();
    query = "SELECT equipe_id, nom, pays, entraineur_principal, stade_domicile FROM Equipe"
    cursor.execute(query)
    teams = [{
        'id': row[0],
        'nom': row[1],
        'pays': row[2],
        'entraineur_principal': row[3],
        'stade_domicile': row[4]
    } for row in cursor.fetchall()]
    connection.close()
    return teams


def create_match(tournament_id, team1_id, team2_id, round):
    connection, cursor = _open_sql_connection()
    cursor.execute("INSERT INTO Parties (tournament_id, team1_id, team2_id, round) VALUES (%s, %s, %s, %s)",
                   (tournament_id, team1_id, team2_id, round))
    match_id = connection.insert_id()
    connection.commit()
    connection.close()
    return match_id


def select_teams_and_players():
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


def insert_match(tournament_id, home_team_id, visitor_team_id):
    connection, cursor = _open_sql_connection()
    sql_query = """
        INSERT INTO Partie (tournoi_id, equipe_locale_id, equipe_visiteur_id, date, lieu)
        VALUES (%s, %s, %s, '2024-05-20', 'Stade par défaut')
    """
    cursor.execute(sql_query, (tournament_id, home_team_id, visitor_team_id))
    match_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return match_id


def select_matches(tournament_id):
    connection, cursor = _open_sql_connection()
    sql_query = """
    SELECT match_id, date, lieu, equipe_locale_id, equipe_visiteur_id, tournoi_id
    FROM Partie
    WHERE tournoi_id = %s
    ORDER BY date;
    """
    cursor.execute(sql_query, (tournament_id,))
    matches = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{
        'match_id': match[0],
        'date': match[1],
        'lieu': match[2],
        'equipe_locale_id': match[3],
        'equipe_visiteur_id': match[4],
        'tournoi_id': match[5]
    } for match in matches]


def update_match_result(match_id, home_team_score, visitor_team_score):
    if home_team_score > visitor_team_score:
        winner = "home"
    elif visitor_team_score > home_team_score:
        winner = "away"
    else:
        winner = "draw"
    # Format the score as a string e.g., "2-1"
    score_resultat = f"{home_team_score}-{visitor_team_score}"

    connection, cursor = _open_sql_connection()
    try:
        query = """
            UPDATE Partie
            SET resultat = %s, winner = %s
            WHERE match_id = %s
        """
        cursor.execute(query, (score_resultat, winner, match_id))
        connection.commit()
    except Exception as e:
        print(f"An error occurred while updating match result: {e}")
    finally:
        cursor.close()
        connection.close()


def fetch_match_results(tournament_id):
    connection, cursor = _open_sql_connection()
    query = """
        SELECT match_id, equipe_locale_id, equipe_visiteur_id, winner
        FROM Partie
        WHERE tournoi_id = %s
    """
    cursor.execute(query, (tournament_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    # Transform the results into a format that includes team IDs and the winner
    match_results = [{
        "match_id": row[0],
        "home_team_id": row[1],
        "away_team_id": row[2],
        "winner": row[3]
    } for row in results]
    return match_results

def select_tournament_by_id(tournament_id):
    connection, cursor = _open_sql_connection()
    cursor.execute("SELECT * FROM tournoi WHERE tournoi_id = %s", (tournament_id,))
    tournament = cursor.fetchone()
    connection.close()
    return tournament


def delete_tournament(tournament_id):
    connection, cursor = _open_sql_connection()
    cursor.execute("DELETE FROM tournoi WHERE tournoi_id = %s", (tournament_id,))
    connection.commit()  # Make sure to commit the transaction
    connection.close()


if __name__ == '__main__':
    select_tournaments()
