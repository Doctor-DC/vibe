import Vue from 'vue'
import Router from 'vue-router'
import App from './App/App.vue'
import Game from './pages/Game.vue'
import Home from './pages/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/game',
      name: 'Game',
      component: Game
    }
  ]
})
