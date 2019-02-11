<template>
  <!-- s  -->
  <section class="content" id="content" v-show="content">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import ExampleContentComponent from '../../components/content/example/example.vue'
// include dependence
export default {
  name: 'Content',
  data () {
    return {
      content: false,
      current: null,
      gold: {
        'example': ExampleContentComponent
      }
      // start datas
      // end datas
    }
  },
  watch: {
    '$store.state.content' (content) {
      if (content === false) {
        this.content = false
        this.current = null
      } else {
        this.content = true
        this.current = this.gold[content]
      }
    }
  },
  components: {
    ExampleContentComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./content.scss";
</style>
