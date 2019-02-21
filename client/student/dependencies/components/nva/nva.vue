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
import Dictionary from '../../modules/Dictionary.class.js'

export default {
  name: 'NvaComponent',
  data () {
    return {
      nav: [{
        name: '课程列表',
        page: 'student-course'
      }],
    }
  },
  created () {
    this.nav = Storage.nav
  },
  watch: {
    '$store.state.nav' (value) {
      this.nav = value
    },
    '$route'(to, from) {
      let nav = Dictionary.navModeExample
      if (Dictionary.navModeHomework.indexOf(to.name) !== -1) nav = Dictionary.navModeHomework

      let index = nav.indexOf(to.name)
      if (index > -1) {
        let result = []
        for (let i = 0; i <= index; i++) {
          result.push({
            name: Dictionary.page[nav[i]],
            page: nav[i]
          })
        }
        this.nav = result
        Storage.nav = result
      }
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
