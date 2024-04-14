import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Tournoi from '../views/TournamentComponent.vue'
import Equipe from '@/views/EquipeComponent.vue'
import Classement from '@/views/Classement.vue'
import Joueur from '@/views/JoueurComponent.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/tournoi',
      name: 'tournoi',
      component: Tournoi
    },
    {
      path: '/equipe',
      name: 'equipe',
      component: Equipe

    },
    {
      path: '/classement',
      name: 'classement',
      component: Classement
    },
    {
      path: '/joueur',
      name: 'joueur',
      component: Joueur
    }
  ]
})

export default router
