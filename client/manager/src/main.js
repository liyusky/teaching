// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Main from './app/main/main.vue'
import Detail from './app/detail/detail.vue'
import Panel from './app/panel/panel.vue'
import Modal from './app/modal/modal.vue'
import Content from './app/content/content.vue'
import Substance from './app/substance/substance.vue'
import Cview from './app/cview/cview.vue'
import Tip from './app/tip/tip.vue'
import router from './router/router.js'
import store from './store/index'
import '../dependencies/sass/_reset.scss'
import '../dependencies/sass/_commom.scss'

Vue.config.productionTip = false

window.manager = new Vue({
  el: '#main',
  router,
  store,
  render: f => f(Main)
})

window.detail = new Vue({
  el: '#detail',
  store,
  render: f => f(Detail)
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

window.content = new Vue({
  el: '#content',
  store,
  render: f => f(Content)
})

window.substance = new Vue({
  el: '#substance',
  store,
  render: f => f(Substance)
})

window.cview = new Vue({
  el: '#cview',
  store,
  render: f => f(Cview)
})

window.tip = new Vue({
  el: '#tip',
  store,
  render: f => f(Tip)
})
