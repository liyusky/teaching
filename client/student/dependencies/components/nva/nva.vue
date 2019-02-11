<template>
  <!-- s  -->
  <p class="nva color-white">
    <span class="arrow" v-for="(item, index) in nav" :key="index" @click="target(index)">{{item.name}}</span>
  </p>
  <!-- s  -->
</template>

<script>
// include dependence
import Router from '../../modules/Router.class.js'
import Storage from '../../modules/Storage.class.js'

export default {
  name: 'NvaComponent',
  data () {
    return {
      nav: [{
        name: '课程列表',
        page: 'student'
      }]
    }
  },
  created () {
    this.nav = Storage.nav
  },
  watch: {
    '$store.state.nav' (value) {
      this.nav = value
    }
  },
  methods: {
    target (index) {
      Storage.adjustNav = (index + 1)
      Router.target = this.nav[index].page
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./nva.scss";
</style>
