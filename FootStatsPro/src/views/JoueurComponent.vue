<template>
<div class="joueurs-container">
    <div class="filtres-container">
        <h2>
          Filtres
        </h2>
        <div class="filtre-position">
          <select @change="onSelectedPosition" name="position" id="choixPosition">
            <option value="None" selected></option>
            <option value="buts">Buts</option>
            <option value="passes">Passes</option>
            <option value="forward">Forward</option>
            <option value="midfielder">Midfielder</option>
            <option value="defender">Defender</option>
            <option value="goalkeeper">Goalkeeper</option>
          </select>
        <h2>Liste des Joueurs de Soccer</h2>
        <table>
          <thead>
            <tr>

              <th>Nom</th>
              <th>Âge</th>
              <th>Position</th>
              <th>Équipe</th>
              <th>Buts</th>
              <th>Passes</th>
              <th>Matchs</th>
              <th>Ratio Buts/Match</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="joueur in joueurs" :key="joueur.joueur_id">

              <td>{{ joueur.nom }}</td>
              <td>{{ joueur.age }}</td>
              <td>{{ joueur.position }}</td>
              <td>{{ joueur.nom_equipe }}</td>
              <td>{{joueur.total_buts}}</td>
              <td>{{joueur.total_passes}}</td>
              <td>{{joueur.nb_matchs}}</td>
              <td>{{calculerRatio(joueur.total_buts, joueur.nb_matchs)}}</td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>
</div>
</template>

<script setup>

import { onMounted, ref } from 'vue';

const joueurs = ref([]);

function calculerRatio(buts, match) {

  if (match == 0) {
    return 0;
  }
  else {
    return (buts/match).toFixed(2);
  }
}

 const getJoueurs = async (position) => {
  try {
    const response = await fetch(`http://localhost:5000/joueur/${position}`);
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    const data = await response.json();
    joueurs.value = data.players;
  } catch (error) {
    console.error("ERREUR LORS DE LA RECUPERATION DES JOUEURS", error);
  }
};

function onSelectedPosition(event) {
  const selected_position = event.target.value;
  getJoueurs(selected_position);
}

onMounted(() => getJoueurs())


</script>


<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

select {
    padding: 8px;
    margin-top: 10px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: white;
    cursor: pointer;
}

select:hover {
    border-color: #888;
}

option {
    padding: 10px;
}



</style>