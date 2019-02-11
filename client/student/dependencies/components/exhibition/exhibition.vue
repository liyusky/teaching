<template>
  <!-- s  -->
  <section class="exhibition">
    <div class="exhibition-title color-white fz-28">{{exhibition.title}}</div>
    <div class="exhibition-banner">
      <img src="../../../src/assets/calss-sign.jpg">
    </div>
    <div class="exhibition-message color-cyan">
      <slot></slot>
    </div>
    <div class="exhibition-btn">
      <button class="btn" @click="target" :disabled="disabled">{{exhibition.btn}}</button>
    </div>
    <div class="exhibition-modal" v-show="show"></div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../modules/Communication.class.js'
import Router from '../../modules/Router.class.js'

export default {
  name: 'ExhibitionComponent',
  props: ['exhibition'],
  data () {
    return {
      show: false,
      disabled: false
    }
  },
  created () {
    console.log(this.exhibition)
    this.getStatus()
  },
  methods: {
    target (exhibition) {
      Communication.lesson = this.exhibition
      Router.push(this.exhibition.page)
    },
    getStatus () {
      let launch = (new Date(this.exhibition.launch)).getTime()
      let deadline = (new Date(this.exhibition.deadline)).getTime()
      let now = (new Date()).getTime()
      if (now < launch) {
        this.disabled = true
        this.show = true
      } else {
        this.disabled = false
        this.show = false
      }
    },
  }
}
</script>

<style lang="sass" scoped>
@import "./exhibition.scss";
</style>
