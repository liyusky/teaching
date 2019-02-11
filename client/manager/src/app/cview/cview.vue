<template>
  <!-- s  -->
  <section class="cview" id="cview" v-show="cview">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import ExampleCviewComponent from '../../components/cview/example/example.vue'
// include dependence
export default {
  name: 'Cview',
  data () {
    return {
      cview: false,
      current: null,
      gold: {
        'example': ExampleCviewComponent
      }
      // start datas
      // end datas
    }
  },
  watch: {
    '$store.state.cview' (cview) {
      if (cview === false) {
        this.cview = false
        this.current = null
      } else {
        this.cview = true
        this.current = this.gold[cview]
      }
    }
  },
  components: {
    ExampleCviewComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./cview.scss";
</style>
