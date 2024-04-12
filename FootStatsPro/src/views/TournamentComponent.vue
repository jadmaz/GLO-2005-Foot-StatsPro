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
            <option v-for="count in [2, 4, 8, 16, 32]" :key="count" :value="count">{{ count }}</option>
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
    <h2> Sélectionner un tournois </h2>
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

    </header>
  </div>
</template>




<script setup>
import { ref, onMounted, computed } from 'vue';
const knownRounds = ref(["1/16 Finals","16 de finale","Quarterfinals","Semifinals","Final", "Winner"]); // Now knownRounds is a reactive reference
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
const bracket = ref({});
const winner = ref(null)
const currentTournamentId = ref(null); // Initialize currentTournamentId
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
        console.log("Tournament added successfully:", data);
        currentTournamentId.value = data.tournoi_id;

        // Fetch the latest list of tournaments from the server,
        // which now includes the newly added tournament.
        await fetchTournamentsFromServer();

        await fetchBracket(data.tournoi_id, tournament.teamCount);
        console.log("VOICI LE BRACKET", bracket.value)
        for (const [round, matches] of Object.entries(bracket.value)) {
         for (const match of matches) {
          const homeTeamId = match[0].id;
          const visitorTeamId = match[1].id;
          const date = "2024-01-01";
          const place = "Exemple Lieu";
          console.log(data.tournoi_id);
          await createMatch(data.tournoi_id, homeTeamId, visitorTeamId, round, date, place);
          await fetchMatches(data.tournoi_id);
      }
    }
      } else {
        console.error("Tournament ID not received:", data);
      }

      // Reset the form fields
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
      // If the response is not OK, throw an error with the response status
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log("Response data:", data);

    // Return the data so it can be used by the caller
    return data;
  } catch (error) {
    console.error('Error sending tournament:', error);
    // Rethrow the error to ensure the caller can catch and handle it
    throw error;
  }
}

const getTeams = async() => {
  console.log("fetching teams");
  try{
    const response = await fetch('http://localhost:5000/equipe')
    if(!response.ok){
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log("teams fetched succesfully", data)
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
    console.log("Fetched Bracket Structure:", data); // Debug output
     bracket.value = parseBracket(data);
     console.log("bracket en json initial", (JSON.stringify(bracket)));
     console.log("bracket en json initial", (JSON.stringify(bracket.value)));
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
        console.log("Matches fetched successfully:", data);
        console.log(matches);
        // Ici, vous pouvez mettre à jour l'état de votre composant Vue avec les matchs récupérés
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
    console.log("Match created:", data);
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
  console.log("Match ID:", matchId);

  const homeTeamScore = prompt(`Enter score for ${match[0].nom}:`);
  const visitorTeamScore = prompt(`Enter score for ${match[1].nom}:`);

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
    console.log("hometeamscore", homeTeamScore)
    console.log("visitorTeam", visitorTeamScore)
    if( homeTeamScore > visitorTeamScore){
      console.log("le id home", homeTeamId);
      console.log("le id away", visitorTeamId);
      await updateStandings(homeTeamId, visitorTeamId)
    }
    else if( homeTeamScore < visitorTeamScore){
      console.log("le id home", homeTeamId);
      console.log("le id away", visitorTeamId);
      await updateStandings(visitorTeamId, homeTeamId)
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
    return await response.json();
  } catch (error) {
    console.error('Error fetching match results:', error);
    return [];
  }
};
const updateBracketWithMatchResults = async (tournamentId, bracketData) => {
  try {
    console.log('Tournament ID:', tournamentId);
    console.log('Initial Bracket:', bracketData);

    const payload = {
      tournamentId,
      bracket: bracketData,
    };

    console.log('Payload sent to server:', JSON.stringify(payload, null, 2));

    const response = await fetch(`http://localhost:5000/update-bracket/${tournamentId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
      throw new Error(`Failed to update bracket with match results. Status: ${response.status}`);
    }
    const updatedData = await response.json();
    console.log('Updated Bracket:', updatedData);

    // Check if a winner has been determined
    if (updatedData['Winner']) {
      console.log(`Winner of the tournament is: ${updatedData['Winner'].nom}`);
      winner.value = updatedData;
      bracket.value.Winner = updatedData['Winner'];
    } else {
      // If no winner yet, continue as before
      let updatedBracket = parseBracket(updatedData);
      bracket.value = updatedBracket; // Update bracket with new structure

      for (const [round, matchesArray] of Object.entries(updatedBracket)) {
        console.log(`Creating matches for round: ${round}`, matchesArray);
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
      console.log("Data from API:", data);
      selectedTournament.value = data.tournament;
      showDeleteButton.value = true;

    } catch (error) {
      console.error('Erreur lors de la récupération des détails du tournoi sélectionné:', error);
    }
  }
};

function parseBracket(rawBracket) {
  // Normalize the rawBracket to only include the rounds you need
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
  background-color: gold; /* Green background */
  color: white; /* White text */
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
  align-items: center; /* Center align the items vertically */
  justify-content: space-around;
  margin: 10px 0;
}
.team {
  margin: 0 10px;
}
body {
  font-family: 'Arial', sans-serif;
  background-color: #f7f7f7; /* Une couleur neutre de fond */
}

/* Styles pour le titre principal */
h2 {
  color: #004d38; /* Une couleur verte foncée */
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

/* Styles pour le formulaire et les listes */
form,
ul {
  background-color: white;
  padding: 1em;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Styles pour le conteneur du bracket */
.bracket {
  background-color: white;
  padding: 1em;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Styles pour chaque round du bracket */
.rounds {
  background-color: #e6ffe6; /* Une couleur verte claire pour évoquer le terrain */
  padding: 0.5em;
  border-radius: 5px;
  margin-bottom: 1em;
}

/* Styles pour les boutons */
button {
  background-color: #00802b; /* Vert foncé pour le bouton */
  color: white;
  border: none;
  padding: 0.5em 1em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #005f1f; /* Une teinte plus foncée au survol */
}

/* Styles pour les équipes et les matchs */
.team {
  font-weight: bold;
}

.match {
  padding: 0.5em;
  border-bottom: 1px solid #ddd; /* Une ligne séparatrice pour chaque match */
}

.vs {
  font-style: italic;
   flex: 1; /* Each child will take up equal space */
  text-align: center; /* Center the text for each child */
}
.vs {
  margin: 0 15px; /* Add some horizontal margin to the 'vs' for spacing */
  font-style: italic;
  flex: none; /* Do not allow the 'vs' to grow, keeping its content width */
}
.generate-next-round {
  background-color: black; /* Black background */
  color: white; /* White text */
  border: none;
  padding: 0.5em 1em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.generate-next-round:hover {
  background-color: #333; /* Darker background on hover */
  color: #ddd; /* Lighter text on hover */
}
.team:first-child {
  text-align: right; /* Right align the text of the first team */
}

.team:last-child {
  text-align: left; /* Left align the text of the second team */
}

/* Ajout d'un petit padding autour des éléments pour l'aération */
label,
input,
select,
ul,
li {
  margin-bottom: 0.5em;
}

/* Spécifique aux listes pour ajouter des puces personnalisées */
ul {
  list-style-type: none;
  padding-left: 1em;
}

li:before {
  content: '⚽'; /* Ajout d'un ballon de soccer avant chaque élément de liste */
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
  flex-wrap: wrap; /* Wrap items to the next line if not enough space */
  margin-bottom: 15px; /* Adds space between rows */
}

/* Set explicit widths for form groups */
.form-group {
  margin-right: 10px; /* Manually set right margin for spacing between form groups */
}

.form-group:nth-child(1) { /* Nom du tournoi */
  width: 30%;
}

.form-group:nth-child(2), /* Date de début */
.form-group:nth-child(3) { /* Date de fin */
  width: 20%;
}

.form-group:nth-child(4), /* Nombre d'équipes */
.form-group:nth-child(5) { /* Lieu */
  width: 25%;
}

/* Remove the right margin from the last form-group in each form-row */
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
