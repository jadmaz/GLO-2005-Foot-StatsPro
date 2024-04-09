import math
from database import (
    insert_tournaments, select_tournaments, delete_tournament,
    select_teams_and_players, select_teams, create_match)
from random import shuffle


def organize_tournament(tournament_id, number_of_teams):
    print(f"Organizing tournament {tournament_id} for {number_of_teams} teams.")

    # Check if the number of teams is valid for a bracket
    valid_team_numbers = [2, 4, 8, 16, 32]  # Ensure this matches with your available bracket structure
    if number_of_teams not in valid_team_numbers:
        raise ValueError("Invalid number of teams for a bracket")

    teams = select_teams()
    print(f"Retrieved {len(teams)} teams from the database.")

    # Raise an error if there are not enough teams
    if len(teams) < number_of_teams:
        raise ValueError("Not enough teams available for the bracket")

    bracket_structure = initialize_bracket_structure(number_of_teams)
    print(f"Bracket structure initialized with rounds: {list(bracket_structure.keys())}")

    # Get the first round name from the bracket structure
    first_round_name = next(iter(bracket_structure))
    first_round_matches = generate_first_round_matches(teams[:number_of_teams])
    print(f"First round matches: {first_round_matches}")

    # Assign matches to the first round in the bracket structure
    bracket_structure[first_round_name].extend(first_round_matches)

    return bracket_structure


def initialize_bracket_structure(number_of_teams):
    # Cette fonction retournera une structure de brackets en fonction du nombre d'équipes.
    rounds_map = {
        2: ['Final'],
        4: ['Semifinals', 'Final'],
        8: ['Quarterfinals', 'Semifinals', 'Final'],
        16: ['16 de finale', 'Quarterfinals', 'Semifinals', 'Final'],
        32: ['1/16 Finals', '16 de finale', 'Quarterfinals', 'Semifinals', 'Final'],
    }
    number_of_rounds = int(math.log2(number_of_teams))

    if number_of_teams not in rounds_map:
        raise ValueError(f"Nombre de teams non valide pour un tournoi: {number_of_teams}")

    rounds_names = rounds_map[number_of_teams]

    rounds_names = rounds_names[-number_of_rounds:]

    bracket_structure = {round_name: [] for round_name in rounds_names}

    print(f"Structure de bracket initialisée avec les rounds: {list(bracket_structure.keys())}")
    return bracket_structure


def generate_first_round_matches(teams):
    shuffle(teams)
    matches = [teams[i:i + 2] for i in range(0, len(teams), 2)]
    print(f"Generated first-round matches: {matches}")
    return matches


def update_bracket_with_results(bracket_structure, match_results):
    print("Début de la mise à jour du bracket avec les résultats des matchs.")
    for round_name, matches in bracket_structure.items():
        print(f"Traitement du round: {round_name}")
        updated_matches = []  # Initialise une nouvelle liste pour stocker les matchs mis à jour

        for match in matches:
            # Assurez-vous que chaque 'match' est une liste de dictionnaires représentant les équipes
            if not match or not isinstance(match, list) or not all(isinstance(team, dict) for team in match):
                print("Format de match invalide.")
                continue

            # Identifier le match_id si présent
            match_id = None
            for m in match:
                for result in match_results:
                    if m['id'] == result['home_team_id'] or m['id'] == result['away_team_id']:
                        match_id = result['match_id']
                        break
                if match_id:
                    break

            # Vérifier le résultat du match par son ID
            if match_id:
                result = next((r for r in match_results if r['match_id'] == match_id), None)
                if result:
                    # Trouver l'ID de l'équipe gagnante
                    winning_team_id = result['winner'] == 'home' and result['home_team_id'] or result['away_team_id']
                    print(f"Équipe gagnante du match {match_id}: {winning_team_id}")

                    # Préparer l'équipe gagnante pour le prochain round
                    next_round = find_next_round(round_name, bracket_structure)
                    if next_round:
                        winning_team_info = next(team for team in match if team['id'] == winning_team_id)
                        updated_matches.append(winning_team_info)
                        print(f"Placement de l'équipe gagnante {winning_team_id} dans le prochain round: {next_round}")
                else:
                    print(f"Aucun résultat trouvé pour le match {match_id}.")
            else:
                print("ID de match non trouvé.")

        # Mettre à jour le bracket_structure avec les matchs du prochain round
        if updated_matches:
            bracket_structure[next_round] = updated_matches

    print("Mise à jour du bracket terminée.")
    print(bracket_structure)


def find_next_round(current_round, bracket_structure):
    print(f"Recherche du prochain round après {current_round}.")
    rounds = list(bracket_structure.keys())
    current_index = rounds.index(current_round)
    if current_index + 1 < len(rounds):
        next_round = rounds[current_index + 1]
        print(f"Prochain round trouvé: {next_round}")
        return next_round
    print("Aucun prochain round trouvé.")
    return None


def place_winner_in_next_round(winning_team_id, next_round, bracket_structure):
    # Recherche d'un match dans le prochain round où placer l'équipe gagnante
    for match in bracket_structure[next_round]:
        if len(match) < 2:
            match.append({'id': winning_team_id, 'match_id': None})  # Ajouter un match_id si nécessaire
            print(f"Équipe {winning_team_id} ajoutée dans un match existant du round {next_round}.")
            return

    # Si tous les matchs du round suivant sont pleins ou si le round est vide, initialiser un nouveau match
    bracket_structure[next_round].append([{'id': winning_team_id, 'match_id': None}])
    print(f"Nouveau match initié avec l'équipe {winning_team_id} dans le round {next_round}.")
