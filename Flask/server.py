from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from database import insert_tournaments, select_tournaments, delete_tournament, select_teams

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


@app.route('/delete-tournament/<int:tournament_id>', methods=['DELETE'])
def remove_tournament(tournament_id):
    delete_tournament(tournament_id)
    return jsonify({'status': 'success', 'message': 'Tournament deleted'})


if __name__ == '__main__':
    app.run()
