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
    <button @click="deleteTournaments(index)">Supprimer</button>
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
      await postTournament(tournament);

      tournaments.value.push(tournament);

      newTournament.value = {
        name: '',
        startDate: '',
        endDate: '',
        teamCount: 0,
        location: ''
      };


      fetchTournamentsFromServer();
    } catch (error) {
      console.error('Erreur lors de l\'ajout du tournoi:', error);
    }
  }
}

const deleteTournaments = (index) => {
  tournaments.value.splice(index, 1)
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

    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Erreur lors de l\'envoi du tournoi:', error);
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
