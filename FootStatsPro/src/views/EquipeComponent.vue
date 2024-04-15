<template>
  <div class="equipes-container">
    <div v-for="equipe in equipes" :key="equipe.id" class="equipe">
      <h2>{{ equipe.nom }}</h2>
      <p>Pays: {{ equipe.pays }}</p>
      <p>Entraîneur: {{ equipe.entraineurPrincipal }}</p>
      <p>Stade: {{ equipe.stadeDomicile }}</p>
      <p>Trophées: {{ equipe.trophees }}</p>
      <h3>Joueurs</h3>
      <ul class="joueurs-liste">
        <li v-for="joueur in equipe.joueurs" :key="joueur.id">
          {{ joueur.nom }} - {{ joueur.position }} - {{ joueur.age }} ans
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
const equipes = ref([]);
const processTeamsData = (rawData) => {
  const teamsMap = new Map();
  rawData.forEach((teamData) => {
const [equipeId, equipeNom, pays, entraineurPrincipal, stadeDomicile, trophees, joueurId, joueurNom, joueurAge, joueurPosition] = teamData;
    if (!teamsMap.has(equipeId)) {
  teamsMap.set(equipeId, {
    id: equipeId,
    nom: equipeNom,
    pays: pays,
    entraineurPrincipal: entraineurPrincipal,
    trophees: trophees,
    stadeDomicile: stadeDomicile,
    joueurs: [],
  });
}
    if (joueurId && joueurNom) {
      const player = {
        id: joueurId,
        nom: joueurNom,
        age: joueurAge,
        position: joueurPosition,
      };
      teamsMap.get(equipeId).joueurs.push(player);
    }
  });
  return Array.from(teamsMap.values());
};
const fetchTeamsFromServer = async () => {
  try {
    const response = await fetch('http://localhost:5000/equipes_and_players');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    equipes.value = processTeamsData(data.teams);
  } catch (error) {
    console.error('Error fetching teams:', error);
  }
};
onMounted(fetchTeamsFromServer);
</script>

<style>
.equipes-container {
  margin-top : 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}
.equipe {
  background-color: #f3f3f3;
  border: 1px solid #ddd;
  border-radius: 10px;
  transition: box-shadow 0.3s ease-in-out;
  padding: 20px;
  width: 300px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.equipe h2 {
  color: #333;
  margin-bottom: 10px;
}
.equipe p {
  color: #666;
  margin-bottom: 5px;
}
.equipe:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); /* L'ombre s'affiche lors du survol */
}
.joueurs-liste {
  list-style-type: none;
  padding: 0;
  margin-top: 10px;
}
.joueurs-liste li {
  background-color: white;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 5px;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
}
</style>