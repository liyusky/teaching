<template>
  <!-- s  -->
  <section class="substance" id="substance" v-show="substance">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import LessonSubstanceComponent from '../../components/substance/lesson/lesson.vue'
// include dependence
export default {
  name: 'Substance',
  data () {
    return {
      substance: false,
      current: null,
      gold: {
        'lesson': LessonSubstanceComponent
      }
    }
  },
  watch: {
    '$store.state.substance' (substance) {
      console.log(substance)
      if (substance === false) {
        this.substance = false
        this.current = null
      } else {
        this.substance = true
        this.current = this.gold[substance]
      }
    }
  },
  components: {
    LessonSubstanceComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./substance.scss";
</style>
