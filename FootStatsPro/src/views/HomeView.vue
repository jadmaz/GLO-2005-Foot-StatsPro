<template>
  <div class="home">
    <section class="intro">
      <h1>Bienvenue sur FootProStats</h1>
      <p>Votre centre de statistiques pour le football professionnel. Suivez les classements, découvrez les tournois en cours, et explorez les statistiques des équipes.</p>
      <div class="links-container">
        <router-link to="/classement" class="intro-link">Voir les Classements</router-link>
        <router-link to="/tournoi" class="intro-link">Explorer les Tournois</router-link>
        <router-link to="/equipe" class="intro-link">Découvrir les Équipes</router-link>
        <router-link to="/joueur/" class="intro-link">Consulter les Statistiques</router-link>
      </div>
    </section>
    <section class="mission">
      <h2>Notre Mission</h2>
      <p>Notre application a été conceptualisée afin de venir en aide aux analystes professionnels et aux entraineurs de ligues de soccer. Celle-ci contient les données des différentes équipes de la ligue, des joueurs qui en font parties, des matchs auxquels ces équipes participent, les tournois au cours desquels les matchs sont joués, et les statistiques associées aux performances des joueurs.</p>
    </section>
        <section class="features">
      <h2>Fonctionnalités Clés</h2>
      <div class="feature-list">
        <div class="feature">
          <h3>Statistiques en Temps Réel</h3>
          <p>Accédez à des données mises à jour instantanément pendant les matchs.</p>
        </div>
        <div class="feature">
          <h3>Analyse Avancée</h3>
          <p>Utilisez nos outils d'analyse pour évaluer la performance des joueurs.</p>
        </div>
        <div class="feature">
          <h3>Historique des Matchs</h3>
          <p>Explorez l'historique complet des matchs pour chaque équipe et joueur.</p>
        </div>
      </div>
    </section>

    <section class="testimonials">
      <h2>Témoignages</h2>
      <div class="testimonial-list">
        <blockquote class="testimonial">
          <p>"Cette plateforme a transformé notre manière de suivre le football professionnel. Un outil indispensable pour notre équipe!"</p>
          <cite>- Jean Dupont, Analyste Sportif</cite>
        </blockquote>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  components: {}
}
</script>

<style scoped>
.home .intro {
  text-align: center;
  padding: 2rem;
}

.intro h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.intro p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.links-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.intro-link {
  background-color: #00802b;
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  transition: background-color 0.3s ease;
}

.intro-link:hover {
  background-color: #005f1f;
}

.mission {
  background-color: #f8f9fa;
  padding: 2rem;
  margin-top: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.mission h2 {
  text-align: left;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.mission p {
  font-size: 1rem;
  line-height: 1.6;
  text-align: justify;
}

.features {
  text-align: center;
  padding: 2rem;
  border-left: 4px solid #005f1f;
}
.feature-list {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}
.feature {
  width: 30%;
  margin-bottom: 2rem;
}


.testimonials {
  background-color: #f8f9fa;
  padding: 2rem;
}
.testimonial-list {

}
.testimonial {
  padding: 1rem;
  margin-bottom: 1rem;
  border-left: 4px solid #005f1f;
  background-color: white;
}
</style>
