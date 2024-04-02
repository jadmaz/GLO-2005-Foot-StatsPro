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



  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const tournaments = ref([]);
const cities = ref([
  { name: 'Tokyo', country: 'Japan' },
  { name: 'New York City', country: 'USA' },
  { name: 'Paris', country: 'France' }
]);

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

      // Assuming data.tournoi_id is available immediately after a successful post
      if (data && data.tournoi_id) {
        // Temporarily add the tournament to the local state for immediate feedback
        tournament.tournoi_id = data.tournoi_id;
        tournaments.value.push({ ...tournament, tournoi_id: data.tournoi_id });
        console.log("Tournament added successfully:", data);

        // Optionally, refresh the list from the server to ensure synchronization
        await fetchTournamentsFromServer();
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
;



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


const fetchTournamentsFromServer = async () => {
  try {
    const response = await fetch('http://localhost:5000/tournaments');
    const data = await response.json();
    tournaments.value = data.tournaments;
  } catch (error) {
    console.error('Erreur lors de la récupération des tournois:', error);
  }
}

onMounted(() => {
  fetchTournamentsFromServer();
});
</script>
