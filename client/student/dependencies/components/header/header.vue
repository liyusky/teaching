<template>
  <!-- s  -->
  <section class="header">
    <div class="header-logo">
      <img src="../../../src/assets/brand.png">
    </div>
    <div class="header-account">
      <div class="header-account">
        <div class="account-type color-white" @click="openDetail">学生专用: {{name}}</div>
        <i class="iconfont icon-arrow-down color-white"></i>
      </div>
      <ul class="header-option-list" v-show="nav">
        <li class="list-item" @click="updateUser">
          <i class=""></i>
          <span class="item-name">修改个人信息</span>
        </li>
        <li class="list-item" @click="quit">
          <i class=""></i>
          <span class="item-name">退出</span>
        </li>
      </ul>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
import Display from '../../modules/Display.class.js'
// include dependence
import Account from '../../modules/Account.class.js'
import Http from '../../modules/Http.class.js';
import Router from '../../modules/Router.class.js';

export default {
  name: 'HeaderComponent',
  data () {
    return {
      nav: false,
      name: Account.name ? Account.name : '未实名',
      role: Account.profession
    }
  },
  methods: {
    updateUser () {
      Display.panel = 'user-update-user'
    },
    openDetail () {
      this.nav = true
    },
    quit () {
      Http.send({
        url: 'Logout'
      }).success(data => {
        this.clear()
        Router.push('login')
      }).fail(data => {
        console.log(data)
      }).default(() => {
      })
    },
    clear () {
      this.$store.commit('account', {})
      this.$store.commit('origin', null)
      this.$store.commit('modal', false)
      this.$store.commit('panel', false)
      this.$store.commit('detail', false)
      this.$store.commit('api', false)
      this.$store.commit('tip', false)
      this.$store.commit('nav', [])
      this.$store.commit('content', false)
      this.$store.commit('communication', {})
      localStorage.clear()
    }
  },
  watch: {
    '$store.state.account' (value) {
      this.name = Account.name
    }
  },
}
</script>

<style lang="sass" scoped>
@import "./header.scss";
</style>
