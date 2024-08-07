import math
from database import (
    insert_tournaments, select_tournaments, delete_tournament,
    select_teams_and_players, select_teams, create_match)
from random import shuffle


def organize_tournament(tournament_id, number_of_teams):

    # Check if the number of teams is valid for a bracket
    valid_team_numbers = [2, 4, 8, 16]  # Ensure this matches with your available bracket structure
    if number_of_teams not in valid_team_numbers:
        raise ValueError("Invalid number of teams for a bracket")

    teams = select_teams()

    if len(teams) < number_of_teams:
        raise ValueError("Not enough teams available for the bracket")

    bracket_structure = initialize_bracket_structure(number_of_teams)

    first_round_name = next(iter(bracket_structure))

    first_round_matches = generate_first_round_matches(teams[:number_of_teams])

    bracket_structure[first_round_name].extend(first_round_matches)
    print("avant le retour:", bracket_structure)
    return bracket_structure


def initialize_bracket_structure(number_of_teams):

    rounds_map = {
        2: ['Final'],
        4: ['Semifinals', 'Final'],
        8: ['Quarterfinals', 'Semifinals', 'Final'],
        16: ['16 de finale', 'Quarterfinals', 'Semifinals', 'Final'],
    }
    number_of_rounds = int(math.log2(number_of_teams))

    if number_of_teams not in rounds_map:
        raise ValueError(f"Nombre de teams non valide pour un tournoi: {number_of_teams}")

    rounds_names = rounds_map[number_of_teams]

    rounds_names = rounds_names[-number_of_rounds:]

    bracket_structure = {round_name: [] for round_name in rounds_names}
    print("roundnames", rounds_names)
    print("bracket structure", bracket_structure)
    print(f"Structure de bracket initialisée avec les rounds: {list(bracket_structure.keys())}")
    return bracket_structure


def generate_first_round_matches(teams):
    shuffle(teams)
    matches = [teams[i:i + 2] for i in range(0, len(teams), 2)]
    print(f"Generated first-round matches: {matches}")
    return matches


def update_bracket_with_results(bracket_structure, match_results):
    bracket_structure = reorder_bracket(bracket_structure)
    bracket_structure['Winner'] = None

    rounds_to_process = [round_name for round_name, matches in bracket_structure.items() if matches]

    for round_name in rounds_to_process:
        print(f"Processing round: {round_name}")
        matches = bracket_structure[round_name]
        winners = process_current_round(matches, match_results)

        next_round_name = find_next_round(round_name, bracket_structure)
        print("next round name", next_round_name)
        if next_round_name and not bracket_structure[next_round_name]:
            advance_winners_to_next_round(winners, next_round_name, bracket_structure)
        elif not next_round_name and winners:
            bracket_structure['Winner'] = winners[0]

        bracket_structure[round_name] = []

    return bracket_structure


def process_current_round(matches, match_results):
    print("Matches:", matches)
    print("Match Results:", match_results)
    winners = []
    for match in matches:
        home_team, away_team = match[0], match[1]
        print("home team", home_team)
        print("away team", away_team)  # We're assuming the first team is home and the second is away
        # Find the match result that corresponds to the current match pair
        result = next((r for r in match_results
                       if r['home_team_id'] == home_team['id'] and r['away_team_id'] == away_team['id']), None)
        if result:
            # Determine which team won and add them to the winners list
            winning_team_id = result['home_team_id'] if result['winner'] == 'home' else result['away_team_id']
            if home_team['id'] == winning_team_id:
                winners.append(home_team)
            else:
                winners.append(away_team)
        # Once the winner is found, no need to check further for this match
    print("Winners:", winners)
    return winners


def advance_winners_to_next_round(winners, next_round_name, bracket_structure):
    if next_round_name == 'Winner':
        bracket_structure[next_round_name] = winners[0]
    else:
        bracket_structure[next_round_name] = [[winners[i], winners[i + 1]] for i in range(0, len(winners), 2)]


def find_match_id(match, match_results):
    for team in match:
        for result in match_results:
            if team['id'] in [result['home_team_id'], result['away_team_id']]:
                return result['match_id']
    return None


def find_winning_team_info(match, result):
    winning_team_id = result['winner'] == 'home' and result['home_team_id'] or result['away_team_id']
    return next((team for team in match if team['id'] == winning_team_id), None)


def process_winners_for_next_round(winners, current_round, bracket_structure):
    next_round_name = find_next_round(current_round, bracket_structure)
    if next_round_name:
        print(f"Next round after {current_round}: {next_round_name}")
        if not bracket_structure[next_round_name]:
            bracket_structure[next_round_name].extend([winners])
            print(f"Advancing winners to next round {next_round_name}: {bracket_structure[next_round_name]}")
        else:
            print(f"Next round {next_round_name} already has matches. No action taken.")
    else:
        print(f"No next round after {current_round}. Update complete.")

    bracket_structure[current_round] = []
    print(f"Cleared matches from round {current_round}.")


def reorder_bracket(bracket):
    print("Starting reorder of the bracket.")

    print("Original bracket structure:", bracket)

    predefined_order = ["16 de finale", "Quarterfinals", "Semifinals", "Final", "Winner"]
    ordered_round_names = [round for round in predefined_order if round in bracket]

    print("Predefined order of rounds:", predefined_order)
    print("Rounds present in the current bracket:", ordered_round_names)

    # Creating a new ordered bracket structure
    ordered_bracket = {round_name: bracket[round_name] for round_name in ordered_round_names}

    print("Bracket after reordering:", ordered_bracket)
    return ordered_bracket


# Remember to include the find_next_round function if not already defined
def find_next_round(current_round, bracket_structure):
    rounds = list(bracket_structure.keys())
    current_index = rounds.index(current_round)
    if current_index + 1 < len(rounds):
        return rounds[current_index + 1]
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
