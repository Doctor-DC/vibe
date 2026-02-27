import Vue from 'vue'
import App from './App/App.vue'
import router from './router'
import '../styles/styles.scss'

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
