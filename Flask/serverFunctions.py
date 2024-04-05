import math
from database import (
    insert_tournaments, select_tournaments, delete_tournament,
    select_teams_and_players, select_teams, create_match)
from random import shuffle


def organize_tournament(tournament_id, number_of_teams):
    print(f"Organizing tournament {tournament_id} for {number_of_teams} teams.")

    # Check if the number of teams is valid for a bracket
    valid_team_numbers = [2, 4, 8, 16, 32]  # Adjusted to valid power of 2 numbers
    if number_of_teams not in valid_team_numbers:
        raise ValueError("Invalid number of teams for a bracket")

    teams = select_teams()
    print(f"Retrieved {len(teams)} teams from the database.")

    # Raise an error if there are not enough teams
    if len(teams) < number_of_teams:
        raise ValueError("Not enough teams available for the bracket")

    bracket_structure = initialize_bracket_structure(number_of_teams)
    print("Initialized bracket structure.")

    first_round_matches = generate_first_round_matches(teams[:number_of_teams])
    print(f"First round matches: {first_round_matches}")

    bracket_structure['16 de finale'].extend(first_round_matches)

    for match in first_round_matches:
        team1_id, team2_id = match
       # match_id = create_match(tournament_id, team1_id, team2_id, "16 de finale")
      #  print(f"Match between team {team1_id} and team {team2_id} created with match ID: {match_id}")

    return bracket_structure


def initialize_bracket_structure(number_of_teams):
    number_of_rounds = math.ceil(math.log2(number_of_teams))
    rounds = ['16 de finale', 'Quarterfinals', 'Semifinals', 'Final']
    bracket_structure = {round_name: [] for round_name in rounds[:number_of_rounds]}
    print(f"Bracket structure initialized with rounds: {list(bracket_structure.keys())}")
    return bracket_structure


def generate_first_round_matches(teams):
    shuffle(teams)
    matches = [teams[i:i + 2] for i in range(0, len(teams), 2)]
    print(f"Generated first-round matches: {matches}")
    return matches
