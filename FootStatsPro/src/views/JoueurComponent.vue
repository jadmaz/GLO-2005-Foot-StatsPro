<template>
<div class="joueurs-container">
    <div class="filtres-container">
        <h2>
          Recherche
        </h2>
        <input id="joeurs-search" type="text"  placeholder="Search joueurs"/>
        <button type="button" onclick="onSearchClick()">Search</button>
        <div id="search-container">

        </div>
      <h3>Filtres</h3>
        <div class="filtre-position">
          <label for="choix">Postition :</label>
          <select @change="onSelectedPosition" name="position" id="choixPosition">
            <option value="None" selected></option>
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
              <th>Équipe ID</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="joueur in joueurs" :key="joueur.joueur_id">

              <td>{{ joueur.nom }}</td>
              <td>{{ joueur.age }}</td>
              <td>{{ joueur.position }}</td>
              <td>{{ joueur.equipe_nom }}</td>
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


</style>