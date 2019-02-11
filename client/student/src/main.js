// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Main from './app/main/main.vue'
import Tip from './app/tip/tip.vue'
import Panel from './app/panel/panel.vue'
import Modal from './app/modal/modal.vue'
import router from './router/router.js'
import store from './store/index'
import '../dependencies/sass/_reset.scss'
import '../dependencies/sass/_commom.scss'

Vue.config.productionTip = false

window.main = new Vue({
  el: '#main',
  router,
  store,
  render: f => f(Main)
})

window.tip = new Vue({
  el: '#tip',
  store,
  render: f => f(Tip)
})

window.panel = new Vue({
  el: '#panel',
  store,
  render: f => f(Panel)
})

window.modal = new Vue({
  el: '#modal',
  store,
  render: f => f(Modal)
})
