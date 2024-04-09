<template>
  <div>
    <h2>Gestion des tournois</h2>

    <form @submit.prevent="addTournament">
      <label>Nom du tournoi:</label>
      <input type="text" v-model="newTournament.name" required />
      <label>Date de début:</label>
      <input type="date" v-model="newTournament.startDate" required />
      <label>Date de fin:</label>
      <input type="date" v-model="newTournament.endDate" required />
      <label>Nombre d'équipes:</label>
      <input type="number" v-model="newTournament.teamCount" min="2" step="2" required />
      <label>Lieu:</label>
      <select v-model="newTournament.location" required>
        <option v-for="(city, index) in cities" :key="index" :value="city.name">
          {{ city.name }}
        </option>
      </select>
      <button type="submit">Ajouter</button>
    </form>

    <ul>
  <li v-for="(tournament, index) in tournaments" :key="index">
    {{ tournament[0] }} - Du {{ new Date(tournament[3]).toLocaleDateString() }} au {{ new Date(tournament[4]).toLocaleDateString() }} -
    {{ tournament[2] }} équipes - Lieu: {{ tournament[1] }}
    <button @click="deleteTournaments(tournament[0])">Supprimer</button>
  </li>
</ul>
  <div>
    <h2>Équipes</h2>
    <ul>
      <li v-for="team in teams" :key="team.id">
        {{ team.nom }} - {{ team.pays }}
      </li>
    </ul>
  </div>
<div v-if="Object.keys(bracket).length">
  <h2>Bracket Structure</h2>
  <div class="bracket">
    <div class="rounds" v-for="(matches, round) in bracket" :key="round">
      <h3>{{ round }}</h3>
      <div class="matches">
        <div class="match" v-for="(match, index) in matches" :key="index">
          <div class="team">{{ match[0].nom }}</div>
          <div class="vs">vs</div>
          <div class="team">{{ match[1].nom }}</div>
          <button @click="playMatch(match, matches)">Play</button>
        </div>
      </div>
    </div>
  </div>
  <!-- Generate Next Round Button -->
  <button @click="updateBracketWithMatchResults(currentTournamentId, bracket)">Generate Next Round</button>
</div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const tournaments = ref([]);
const teams = ref([]);
const matches = ref([]);
const cities = ref([
  { name: 'Tokyo', country: 'Japan' },
  { name: 'New York City', country: 'USA' },
  { name: 'Paris', country: 'France' }
]);
const bracket = ref({});
const currentTournamentId = ref(null); // Initialize currentTournamentId



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
    bracket.value = data;
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

    if (!response.ok) {
      throw new Error('Failed to play match');
    }

    const data = await response.json();
    console.log("Match played:", data);

  } catch (error) {
    console.error('Error playing match:', error);
  }
};



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
const updateBracketWithMatchResults = async (tournamentId, bracket) => {
  try {
    // Debug: Log the tournamentId and the initial state of the bracket
    console.log('Tournament ID:', tournamentId);
    console.log('Initial Bracket:', bracket);

    const payload = {
      tournamentId,
      bracket, // Send the current bracket structure as part of the request payload
    };

    // Debug: Log the payload to ensure it's correctly structured
    console.log('Payload sent to server:', JSON.stringify(payload, null, 2));

    const response = await fetch(`http://localhost:5000/update-bracket/${tournamentId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload), // Convert the JavaScript object to a JSON string
    });

    // Debug: Check the response status
    console.log('Response status:', response.status);

    if (!response.ok) {
      throw new Error(`Failed to update bracket with match results. Status: ${response.status}`);
    }

    const updatedBracket = await response.json(); // Receive the updated bracket structure

    // Debug: Log the updated bracket to verify changes
    console.log('Updated Bracket:', updatedBracket);

    bracket.value = updatedBracket;
    setcur// Assuming you're using Vue and have a reactive variable for the bracket
    console.log('Bracket successfully updated with match results:', updatedBracket);
  } catch (error) {
    console.error('Error updating bracket:', error);
  }
};



onMounted(() => {
  fetchTournamentsFromServer();
  getTeams();
});
</script>

<style scoped>
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
  justify-content: space-between;
  margin: 10px 0;
}
.team {
  margin: 0 10px;
}
</style>
