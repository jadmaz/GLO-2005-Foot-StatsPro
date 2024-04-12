from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from Flask.serverFunctions import organize_tournament, update_bracket_with_results
from database import insert_tournaments, select_tournaments, delete_tournament, select_teams_and_players, select_teams, \
    insert_match, select_matches, update_match_result, fetch_match_results, select_tournament_by_id, \
    update_classement_table, select_standings

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


@app.route("/equipes_and_players", methods=['GET'])
def get_teams_and_players():
    teams = select_teams_and_players()
    return jsonify({"teams": teams})


@app.route("/classement/fetchstandings", methods=['GET'])
def get_standings():
    standings = select_standings()
    print(standings)
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
def get_match_results(tournament_id):
    try:
        results = fetch_match_results(tournament_id)
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


@app.route("/organize-tournament/<int:tournament_id>/<int:number_of_teams>", methods=['GET'])
def get_tournament_bracket(tournament_id, number_of_teams):
    try:
        # Assuming `organize_tournament` returns the bracket structure
        print("getting tournament bracket: ", tournament_id)
        bracket = organize_tournament(tournament_id, number_of_teams)
        print("avant le retour du FETCH", bracket)
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
    print(tournament_id)
    data = request.get_json()
    print("bracket structure", data)

    # Extract the bracket structure from the request
    bracket_structure = data['bracket']

    # Fetch the latest match results for the tournament
    match_results = fetch_match_results(tournament_id)
    print("match results", match_results)

    # Ensure the match results are properly formatted
    if match_results is None:
        return jsonify({"error": "Unable to retrieve match results"}), 400

    # Update the bracket based on the match results
    updated_bracket_structure = update_bracket_with_results(bracket_structure, match_results)
    print("le bon", updated_bracket_structure)

    # Return the updated bracket structure as a response
    return jsonify(updated_bracket_structure), 200


def updatedatabase(tournamentid, winner):
    # logique d'updating du database avec le winner
    pass


if __name__ == '__main__':
    app.run()
