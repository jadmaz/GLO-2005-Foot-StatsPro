from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from Flask.serverFunctions import organize_tournament, update_bracket_with_results
from database import *


app = Flask(__name__)
CORS(app)


@app.route("/add-tournaments", methods=['POST'])
def add_tournaments():
    data = request.json

    new_tournament_data = data.get("newTournament")
    if new_tournament_data:
        name = new_tournament_data.get("name")
        location = new_tournament_data.get("location")
        team_count = new_tournament_data.get("teamCount")
        start_date = new_tournament_data.get("startDate")
        end_date = new_tournament_data.get("endDate")
        tournoi_id = insert_tournaments(name, location, team_count, start_date, end_date)
        organize_tournament(tournoi_id, new_tournament_data['teamCount'])

        response = {
            "status": 200,
            "tournoi_id": tournoi_id,
        }
    else:
        response = {
            "status": 400,
            "message": "Invalid data format. 'newTournament' object not found."
        }

    return jsonify(response)


@app.route("/tournaments", methods=['GET'])
def get_tournaments():
    tournaments = select_tournaments()
    return jsonify({"tournaments": tournaments})


@app.route("/equipe", methods=['GET'])
def get_teams():
    teams = select_teams()
    return jsonify({"teams": teams})


@app.route("/equipe/<int:id>", methods=['GET'])
def get_team_by_id(id):
    team = select_team_by_id(id)
    if team:
        return jsonify({"team": team})
    else:
        return jsonify({"message": "Équipe non trouvée"}), 404


@app.route("/classement/fetchpercentage/<int:team1_id>/<int:team2_id>", methods=['GET'])
def get_classements_percentage(team1_id, team2_id):
    results = get_percentage_wins(team1_id, team2_id)
    return jsonify(results)

@app.route("/equipes_and_players", methods=['GET'])
def get_teams_and_players():
    teams = select_teams_and_players()
    return jsonify({"teams": teams})


@app.route("/classement/fetchstandings", methods=['GET'])
def get_standings():
    standings = select_standings()
    return jsonify({"standings": standings})


@app.route("/create-match", methods=['POST'])
def create_match():
    data = request.json
    tournament_id = data['tournamentId']
    home_team_id = data['homeTeamId']
    visitor_team_id = data['visitorTeamId']

    match_id = insert_match(tournament_id, home_team_id, visitor_team_id)

    return jsonify({"matchId": match_id}), 200


@app.route("/matches/<int:tournament_id>", methods=['GET'])
def get_matches(tournament_id):
    matches = select_matches(tournament_id)
    return jsonify(matches)


@app.route("/matches/results/<int:tournament_id>", methods=['GET'])
def get_match_results_with_team_names(tournament_id):
    try:
        results = fetch_match_results(tournament_id)
        for result in results:
            result['home_team_name'] = get_team_name_by_id(result['home_team_id'])
            result['away_team_name'] = get_team_name_by_id(result['away_team_id'])
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/play-match/<int:match_id>', methods=['POST'])
def play_match(match_id):
    data = request.json
    home_team_score = int(data['homeTeamScore'])
    visitor_team_score = int(data['visitorTeamScore'])

    update_match_result(match_id, home_team_score, visitor_team_score)

    return jsonify({"message": "Match updated successfully"}), 200


@app.route('/update-standings', methods=['POST'])
def update_standings():
    data = request.json
    winner_id = data.get('winnerId')
    loser_id = data.get('loserId')

    update_classement_table(winner_id, loser_id)

    return jsonify({"message": "Standings updated successfully"})


@app.route("/update-tournament-winner/<int:tournament_id>", methods=['PUT'])
def update_winner(tournament_id):
    try:
        data = request.json
        winner_id = data.get('winner_id')
        update_winner_in_tournament_table(tournament_id, winner_id)

        return jsonify({"message": "Winner updated successfully"}), 200
    except Exception as e:
        print(f"An error occurred while updating winner for tournament ID {tournament_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/organize-tournament/<int:tournament_id>/<int:number_of_teams>", methods=['GET'])
def get_tournament_bracket(tournament_id, number_of_teams):
    try:
        bracket = organize_tournament(tournament_id, number_of_teams)
        return bracket, 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/delete-tournament/<int:tournament_id>', methods=['DELETE'])
def remove_tournament(tournament_id):
    delete_tournament(tournament_id)
    return jsonify({'status': 'success', 'message': 'Tournament deleted'})


@app.route("/tournaments/<tournament_id>", methods=['GET'])
def get_tournament_by_id(tournament_id):
    tournament = select_tournament_by_id(tournament_id)
    return jsonify({"tournament": tournament})


@app.route('/update-bracket/<int:tournament_id>', methods=['POST'])
def api_update_bracket(tournament_id):
    data = request.get_json()
    bracket_structure = data['bracket']
    match_results = fetch_match_results(tournament_id)
    if match_results is None:
        return jsonify({"error": "Unable to retrieve match results"}), 400
    updated_bracket_structure = update_bracket_with_results(bracket_structure, match_results)
    return jsonify(updated_bracket_structure), 200



@app.route('/joueur/<string:position>', methods=['GET'])
def get_players(position):
    players = select_players(position)
    response = {
        "status": 200,
        "players": players
    }
    return jsonify({"players": players})




if __name__ == '__main__':
    app.run()
