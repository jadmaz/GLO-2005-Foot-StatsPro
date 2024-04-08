from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from Flask.serverFunctions import organize_tournament
from database import insert_tournaments, select_tournaments, delete_tournament, select_teams_and_players, select_teams

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


@app.route("/organize-tournament/<int:tournament_id>/<int:number_of_teams>", methods=['GET'])
def get_tournament_bracket(tournament_id, number_of_teams):
    try:
        # Assuming `organize_tournament` returns the bracket structure
        bracket = organize_tournament(tournament_id, number_of_teams)
        return jsonify(bracket), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/delete-tournament/<int:tournament_id>', methods=['DELETE'])
def remove_tournament(tournament_id):
    delete_tournament(tournament_id)
    return jsonify({'status': 'success', 'message': 'Tournament deleted'})


if __name__ == '__main__':
    app.run()
