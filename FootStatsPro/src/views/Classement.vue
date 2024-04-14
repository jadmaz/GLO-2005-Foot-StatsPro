<template>
  <div class="classement-container">
    <h1>Classement des Équipes</h1>
    <table>
      <thead>
        <tr>
          <th>Position</th>
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
        <tr v-for="(team, index) in standings" :key="team[1]">
          <td>{{index + 1}}</td>
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
      <div class="match-selector">
    <select v-model="selectedTeam1">
      <option v-for="team in teams" :value="team.id" :key="team.id">{{ team.nom }}</option>
    </select>
    <span> vs </span>
    <select v-model="selectedTeam2">
      <option v-for="team in teams" :value="team.id" :key="team.id">{{ team.nom }}</option>
    </select>
    <button @click="fetchMatchWinPercentage">Afficher le ratio</button>
  </div>

  <div v-if="matchResults">
  <h3>Résultats de confrontation:</h3>
  <div v-if="matchResults[0][2] === '0.00' && matchResults[1][2] === '0.00'">
    <p>Les équipes {{ matchResults[0][1] }} et {{ matchResults[1][1] }} n'ont jamais joué l'une contre l'autre.</p>
  </div>
  <div v-else>
    <p v-for="(result, index) in matchResults" :key="index">
      {{ result[1] }} : {{ result[2] }}% de victoire
    </p>
  </div>
</div>
</div>
</template>



<script setup>
import { ref, onMounted } from 'vue';


const standings = ref([]);
const teams = ref([]);
const selectedTeam1 = ref(null);
const selectedTeam2 = ref(null);
const matchResults = ref(null);


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

async function fetchMatchWinPercentage() {
  if (!selectedTeam1.value || !selectedTeam2.value || selectedTeam1.value === selectedTeam2.value) {
    alert('Veuillez sélectionner deux équipes différentes.');
    return;
  }
  try {
    const url = `http://localhost:5000/classement/fetchpercentage/${selectedTeam1.value}/${selectedTeam2.value}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch match win percentages');
    }
    matchResults.value = await response.json();
    console.log("values", matchResults.value);
  } catch (error) {
    console.error('Error fetching match win percentages:', error);
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

onMounted(() => {
  fetchStandings();
  getTeams()
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

.match-selector {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.match-selector select {
  padding: 10px;
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: white;
}

.match-selector span {
  font-weight: bold;
  margin: 0 10px;
}

.match-selector button {
  padding: 10px 20px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.match-selector button:hover {
  background-color: #45a049;
}

h3 {
  margin-top: 20px;
  text-align: center;
}

p {
  margin: 5px 0;
  text-align: center;
  color: #333;
  font-size: 1.1em;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .match-selector {
    flex-direction: column;
  }

  .match-selector select,
  .match-selector button {
    width: 100%;
    margin-top: 10px;
  }

  .match-selector span {
    display: none;
  }
}
</style>

