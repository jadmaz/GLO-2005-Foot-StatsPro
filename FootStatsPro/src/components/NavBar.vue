<template>
  <nav class="navbar">
    <label class="logo">FootProStats</label>
    <ul class="nav-links">
      <li>
        <router-link to="/">Accueil</router-link>
      </li>
      <li>
        <router-link to="/classement">Classement</router-link>
      </li>
      <li>
        <router-link to="/tournoi">Tournoi</router-link>
      </li>
      <li>
        <router-link to="/equipe">Équipe</router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  components: {}
}
</script>

<style>
.navbar {
  background: lightgray;
  height: 80px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo {
  color: black;
  font-size: 24px;
  font-weight: bold;
}

.nav-links {
  list-style: none;
  display: flex;
  justify-content: center; /* Centrer les éléments horizontalement */
  flex: 1;
}

.nav-links li {
  margin-right: 20px;
}

.nav-links li:last-child {
  margin-right: 0;
}

.nav-links li a {
  color: black;
  text-decoration: none;
  font-size: 16px;
  padding: 10px;
}

.nav-links li a:hover {
  background-color: gray;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}
</style>
