<template>
  <div>
   <h2>Gestion des tournois</h2>
    <form @submit.prevent="addTournament" class="tournament-form">
      <div class="form-row">
        <div class="form-group">
          <label for="tournamentName">Nom du tournoi:</label>
          <input id="tournamentName" type="text" v-model="newTournament.name" required />
        </div>
        <div class="form-group">
          <label for="startDate">Date de début:</label>
          <input id="startDate" type="date" v-model="newTournament.startDate" required />
        </div>
        <div class="form-group">
          <label for="endDate">Date de fin:</label>
          <input id="endDate" type="date" v-model="newTournament.endDate" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="teamCount">Nombre d'équipes:</label>
          <select id="teamCount" v-model="newTournament.teamCount" required>
            <option v-for="count in [2, 4, 8, 16]" :key="count" :value="count">{{ count }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="location">Lieu:</label>
          <select id="location" v-model="newTournament.location" required>
            <option v-for="(city, index) in cities" :key="index" :value="city.name">{{ city.name }}</option>
          </select>
        </div>
      </div>
      <button type="submit">Créer</button>
    </form>

    <div v-if="Object.keys(bracket).length">
      <h2>Bracket Structure</h2>
      <div class="bracket" :key="updateKey">
        <div v-for="(matches, roundName) in bracket" :key="roundName">
          <template v-if="roundName === 'Winner' && winner">
            <div class="winner-info">
              <h3>Winner: {{ bracket.Winner.nom }}</h3>
              <p>Coach: {{ bracket.Winner.entraineur_principal }}</p>
              <p>Country: {{ bracket.Winner.pays }}</p>
              <p>Home Stadium: {{ bracket.Winner.stade_domicile }}</p>
            </div>
          </template>
          <div v-else class="rounds">
            <template v-if="roundName !== 'Winner'">
            <h3>{{ roundName }}</h3>
            <div class="matches">
              <div v-for="(match, index) in matches" :key="index">
                <div class="match">
                  <div class="team">{{ match[0]?.nom || 'TBD' }}</div>
                  <div class="vs">vs</div>
                  <div class="team">{{ match[1]?.nom || 'TBD' }}</div>
                  <button v-if="match[0] && match[1] && !match.played" @click="playMatch(match)">
                    Play
                  </button>
                </div>
              </div>
              <div v-if="!matches.length">No matches scheduled for {{ roundName }}</div>
            </div>
            <button
              v-if="matches.length && roundName !== 'Final'"
              @click="updateBracketWithMatchResults(currentTournamentId, bracket)"
              class="generate-next-round"
            >
              Generate Next Round
            </button>
            <button
              v-if="matches.length && roundName === 'Final'"
              @click="updateBracketWithMatchResults(currentTournamentId, bracket)"
              class="generate-next-round"
            >
              Conclude Tournament
            </button>
          </template>
          </div>
        </div>
      </div>
    </div>
    <h2>Sélectionner un tournoi</h2>
    <select v-model="selectedTournamentId" @change="fetchSelectedTournamentDetails">
      <option value="" disabled>Sélectionner un tournoi</option>
      <option v-for="(tournament, index) in tournaments" :key="tournament[0]" :value="tournament[0]">
        {{ tournament[1] }}
      </option>
    </select>
    <button v-if="showDeleteButton" @click="deleteTournaments(selectedTournamentId)">Supprimer</button>

    <header v-if="selectedTournament">
      <h3>{{ selectedTournament[1] }}</h3>
      <p>Du {{ new Date(selectedTournament[4]).toLocaleDateString() }} au {{ new Date(selectedTournament[5]).toLocaleDateString() }}</p>
      <p>{{ selectedTournament[3] }} équipes</p>
      <p>Lieu: {{ selectedTournament[2] }}</p>
  <p v-if="selectedTournament[6] && winnerName">Gagnant: {{ winnerName.nom }}</p>
      <p v-else>Pas encore de gagnant</p>

    <div v-if="matches.length">
  <h2>Résultats des matchs</h2>
  <ul>
    <li v-for="(match, index) in matches" :key="index">
      <p>Match {{ index + 1 }}:</p>
      <p>{{ match.home_team_name }} {{ match.resultat }} {{ match.away_team_name }}</p>
    </li>
  </ul>
</div>
</header>
  </div>
</template>




<script setup>
import { ref, onMounted, computed } from 'vue';
const knownRounds = ref(["1/16 Finals","16 de finale","Quarterfinals","Semifinals","Final", "Winner"]);
const updateKey = ref(0);
const tournaments = ref([]);
const teams = ref([]);
const matches = ref([]);
const cities = ref([
  { name: 'Tokyo', country: 'Japan' },
  { name: 'New York City', country: 'USA' },
  { name: 'Paris', country: 'France' }
]);
const showDeleteButton = ref(false);
const selectedTournament = ref(null);
const winnerName = ref(null);
const bracket = ref({});
const winner = ref(null)
const currentTournamentId = ref(null);
const selectedTournamentId = ref(null);
const newTournament = ref({
  name: '',
  startDate: '',
  endDate: '',
  teamCount: 0,
  location: ''
});

const addTournament = async () => {
  if (
    newTournament.value.name &&
    newTournament.value.startDate &&
    newTournament.value.endDate &&
    newTournament.value.teamCount &&
    newTournament.value.location
  ) {
    const tournament = {
      name: newTournament.value.name,
      startDate: newTournament.value.startDate,
      endDate: newTournament.value.endDate,
      teamCount: newTournament.value.teamCount,
      location: newTournament.value.location
    };

    try {
      const data = await postTournament(tournament);
      if (data && data.tournoi_id) {
        currentTournamentId.value = data.tournoi_id;


        await fetchTournamentsFromServer();

        await fetchBracket(data.tournoi_id, tournament.teamCount);
        for (const [round, matches] of Object.entries(bracket.value)) {
         for (const match of matches) {
          const homeTeamId = match[0].id;
          const visitorTeamId = match[1].id;
          const date = "2024-01-01";
          const place = "Exemple Lieu";
          await createMatch(data.tournoi_id, homeTeamId, visitorTeamId, round, date, place);
          await fetchMatches(data.tournoi_id);
      }
    }
      } else {
        console.error("Tournament ID not received:", data);
      }

      newTournament.value = {
        name: '',
        startDate: '',
        endDate: '',
        teamCount: 0,
        location: ''
      };

    } catch (error) {
      console.error("Error adding tournament:", error);
    }
  }
};
const deleteTournaments = async (tournamentId) => {
  try {
    const response = await fetch(`http://localhost:5000/delete-tournament/${tournamentId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      // Remove the tournament with the matching ID from the local state
      tournaments.value = tournaments.value.filter(t => t.tournoi_id !== tournamentId);
      await fetchTournamentsFromServer();
    } else {
      console.error('Failed to delete the tournament');
    }
  } catch (error) {
    console.error('Error during deletion:', error);
  }
}


async function postTournament(tournament) {
  const postUrl = 'http://localhost:5000/add-tournaments';
  try {
    const response = await fetch(postUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        newTournament: tournament
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();



    return data;
  } catch (error) {
    console.error('Error sending tournament:', error);
    throw error;
  }
}

const getTeams = async() => {
  try{
    const response = await fetch('http://localhost:5000/equipe')
    if(!response.ok){
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    teams.value = data.teams ;
  }
  catch (error){
    console.error("fetching failed");
  }
};

const fetchTournamentsFromServer = async () => {
  try {
    const response = await fetch('http://localhost:5000/tournaments');
    const data = await response.json();
    tournaments.value = data.tournaments;
  } catch (error) {
    console.error('Erreur lors de la récupération des tournois:', error);
  }
}

const fetchBracket = async (tournamentId, numberOfTeams) => {
  try {
    const response = await fetch(`http://localhost:5000/organize-tournament/${tournamentId}/${numberOfTeams}`);
    if (!response.ok) {
      throw new Error('Failed to fetch bracket structure');
    }
    const data = await response.json();
     bracket.value = parseBracket(data);
  } catch (error) {
    console.error('Error fetching bracket structure:', error);
  }
};

const fetchMatches = async (tournamentId) => {
    try {
        const response = await fetch(`http://localhost:5000/matches/${tournamentId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch matches');
        }
        const data = await response.json();
        matches.value = data
    } catch (error) {
        console.error('Error fetching matches:', error);
    }
};
const createMatch = async (tournamentId, homeTeamId, visitorTeamId, round) => {

    const response = await fetch('http://localhost:5000/create-match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tournamentId, homeTeamId, visitorTeamId, round })
    });
    const data = await response.json();
};

const playMatch = async (match) => {
  // Assuming match is an array with two elements: [team1, team2]
  const homeTeamId = match[0].id;
  const visitorTeamId = match[1].id;

  // Find the match in the matches.value array that involves both teams
  const foundMatch = matches.value.find(m =>
    (m.equipe_locale_id === homeTeamId && m.equipe_visiteur_id === visitorTeamId) ||
    (m.equipe_locale_id === visitorTeamId && m.equipe_visiteur_id === homeTeamId));

  if (!foundMatch) {
    console.error("Match not found");
    return;
  }

  const matchId = foundMatch.match_id;

  let homeTeamScore = "";
  let visitorTeamScore = "";

  while (homeTeamScore === visitorTeamScore) {
    homeTeamScore = prompt(`Enter score for ${match[0].nom}:`);

    while (isNaN(homeTeamScore)) {
      homeTeamScore = prompt("Please enter a valid score for the home team (a number):");
    }

    visitorTeamScore = prompt(`Enter score for ${match[1].nom}:`);

    while (isNaN(visitorTeamScore)) {
      visitorTeamScore = prompt("Please enter a valid score for the visitor team (a number):");
    }

    if (homeTeamScore === visitorTeamScore) {
      alert("Scores cannot be equal. Please enter different scores.");
    }

  }

  try {
    const response = await fetch(`http://localhost:5000/play-match/${matchId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ homeTeamScore, visitorTeamScore })
    });
    match.played = true

    if (!response.ok) {
      throw new Error('Failed to play match');
    }

    const data = await response.json();
    console.log("Match played:", data);

  } catch (error) {
    console.error('Error playing match:', error);
  }



  if (parseInt(homeTeamScore) > parseInt(visitorTeamScore)) {

    await updateStandings(homeTeamId, visitorTeamId);
  } else {

    await updateStandings(visitorTeamId, homeTeamId);
  }
};

const updateStandings = async (winnerId, loserId) => {
  try {
    const response = await fetch(`http://localhost:5000/update-standings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ winnerId, loserId })
    });

    if (!response.ok) {
      throw new Error("Problem updating standings");
    }

    const data = await response.json();
    console.log("Standings updated", data);
  } catch (error) {
    console.error('Error updating standings:', error);
  }
}

const fetchMatchResults = async (tournamentId) => {
  try {
    const response = await fetch(`http://localhost:5000/matches/results/${tournamentId}`);
    if (!response.ok) throw new Error('Failed to fetch match results');
    const matchResults = await response.json();


    matches.value = matchResults;

  } catch (error) {
    console.error('Error fetching match results:', error);
    matches.value = [];
  }
};


const updateWinnerInTournamentTable = async (tournamentId, winner_id) => {
  try {
    const payload = {
      winner_id,
    };

    const response = await fetch(`http://localhost:5000/update-tournament-winner/${tournamentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });


    if (!response.ok) {
      throw new Error(`Failed to update winner in tournament table. Status: ${response.status}`);
    }
  } catch (error) {
    console.error('Error updating winner in tournament table:', error);
  }
};


const updateBracketWithMatchResults = async (tournamentId, bracketData) => {
  try {

    const payload = {
      tournamentId,
      bracket: bracketData,
    };


    const response = await fetch(`http://localhost:5000/update-bracket/${tournamentId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });


    if (!response.ok) {
      throw new Error(`Failed to update bracket with match results. Status: ${response.status}`);
    }
    const updatedData = await response.json();


    // Check if a winner has been determined
    if (updatedData['Winner']) {
      winner.value = updatedData;
      bracket.value.Winner = updatedData['Winner'];
      await updateWinnerInTournamentTable(tournamentId, updatedData['Winner'].id)
    } else {
      // If no winner yet, continue as before
      let updatedBracket = parseBracket(updatedData);
      bracket.value = updatedBracket; // Update bracket with new structure

      for (const [round, matchesArray] of Object.entries(updatedBracket)) {
        for (const match of matchesArray) {
          const homeTeamId = match[0]?.id;
          const visitorTeamId = match[1]?.id;
          if(homeTeamId && visitorTeamId) {
            const date = "2024-01-01"; // Placeholder date, adjust as necessary
            const place = "Example Venue"; // Placeholder venue, adjust as necessary
            await createMatch(tournamentId, homeTeamId, visitorTeamId, round, date, place);
          }
        }
      }

      await fetchMatches(tournamentId); // Fetch updated matches
      updateKey.value++; // Trigger UI updates if necessary
    }
  } catch (error) {
    console.error('Error updating bracket with match results:', error);
  }
};


const fetchSelectedTournamentDetails = async () => {
  if (selectedTournamentId.value) {
    try {
      const response = await fetch(`http://localhost:5000/tournaments/${selectedTournamentId.value}`);
      const data = await response.json();
      selectedTournament.value = data.tournament;
      showDeleteButton.value = true;


      if (data.tournament[6]) {
        winnerName.value = await fetchTeamById(data.tournament[6]);

      }

      await fetchMatchResults(selectedTournamentId.value);


    } catch (error) {
      console.error('Erreur lors de la récupération des détails du tournoi sélectionné:', error);
    }
  }
}

const fetchTeamById = async (teamId) => {
  try {
    const response = await fetch(`http://localhost:5000/equipe/${teamId}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch team with ID ${teamId}`);
    }
    const data = await response.json();
    if (!data.team) {
      throw new Error(`Team data not found for ID ${teamId}`);
    }
    return data.team;
  } catch (error) {
    console.error('Error fetching team:', error);
    return null;
  }
};

function parseBracket(rawBracket) {
  const normalizedBracket = {};
  knownRounds.value.forEach(round => {
    normalizedBracket[round] = rawBracket[round] || [];
  });
  return normalizedBracket;
}

onMounted(() => {
  getTeams()
  fetchTournamentsFromServer();
});
</script>

<style scoped>

.winner-info {
  padding: 20px;
  background-color: gold;
  color: white;
  border-radius: 8px;
  text-align: center;
  margin: 20px 0;
}

.bracket {
  display: flex;
  flex-direction: row;
  justify-content: left;
}
.rounds {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 20px;
}
.matches {
  margin-bottom: 50px;
}
.match {
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin: 10px 0;
}
.team {
  margin: 0 10px;
}
body {
  font-family: 'Arial', sans-serif;
  background-color: #f7f7f7;
}


h2 {
  color: #004d38;
  font-size: 1.5em;
  margin-bottom: 0.5em;
}


form,
ul {
  background-color: white;
  padding: 1em;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


.bracket {
  background-color: white;
  padding: 1em;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


.rounds {
  background-color: #e6ffe6;
  padding: 0.5em;
  border-radius: 5px;
  margin-bottom: 1em;
}


button {
  background-color: #00802b;
  color: white;
  border: none;
  padding: 0.5em 1em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #005f1f;
}

.team {
  font-weight: bold;
}

.match {
  padding: 0.5em;
  border-bottom: 1px solid #ddd;
}

.vs {
  font-style: italic;
   flex: 1;
  text-align: center;
}
.vs {
  margin: 0 15px;
  font-style: italic;
  flex: none;
}
.generate-next-round {
  background-color: black;
  color: white;
  border: none;
  padding: 0.5em 1em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.generate-next-round:hover {
  background-color: #333;
  color: #ddd;
}
.team:first-child {
  text-align: right;
}

.team:last-child {
  text-align: left;
}


label,
input,
select,
ul,
li {
  margin-bottom: 0.5em;
}


ul {
  list-style-type: none;
  padding-left: 1em;
}

li:before {
  content: '⚽';
  margin-right: 0.5em;
}

.tournament-management {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 15px;
}


.form-group {
  margin-right: 10px;
}

.form-group:nth-child(1) {
  width: 30%;
}

.form-group:nth-child(2),
.form-group:nth-child(3) {
  width: 20%;
}

.form-group:nth-child(4),
.form-group:nth-child(5) {
  width: 25%;
}


.form-row .form-group:last-child {
  margin-right: 0;
}

input[type="text"],
input[type="date"],
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
