<template>
  <div class="classement-container">
    <h1>Classement des Équipes</h1>
    <table>
      <thead>
        <tr>
          <th>Saison</th>
          <th>Équipe</th>
          <th>Victoires</th>
          <th>Défaites</th>
          <th>Pays</th>
          <th>Entraîneur Principal</th>
          <th>Stade</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="team in standings" :key="team[1]">
          <td>{{ team[0] }}</td> <!-- Saison -->
          <td>{{ team[2] }}</td> <!-- Nom de l'équipe -->
          <td>{{ team[6] }}</td> <!-- Nombre de victoires -->
          <td>{{ team[7] }}</td> <!-- Nombre de défaites -->
          <td>{{ team[3] }}</td> <!-- Pays -->
          <td>{{ team[4] }}</td> <!-- Entraîneur Principal -->
          <td>{{ team[5] }}</td> <!-- Stade -->
        </tr>
      </tbody>
    </table>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';

// Exemple de données reçues, à remplacer par la récupération des données réelles
const standings = ref([]);

// Fonction fictive pour récupérer les données du classement
async function fetchStandings() {
  try {
    const response = await fetch('http://localhost:5000/classement/fetchstandings'); // Remplacez par votre URL d'API
    if (!response.ok) {
      throw new Error('Failed to fetch standings');
    }
    standings.value = (await response.json()).standings;


    console.log(standings.value)
    console.log(JSON.stringify(standings.value))
  } catch (error) {
    console.error('Error fetching standings:', error);
  }
}

onMounted(() => {
  fetchStandings();
});
</script>

<style scoped>
.classement-container {
  margin: 20px;
  font-family: Arial, sans-serif;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #eee;
}
</style>
