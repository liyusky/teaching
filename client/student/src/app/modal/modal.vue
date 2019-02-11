<template>
  <!-- s  -->
  <section class="modal" id="modal" v-show="modal">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import SchoolSelectModalComponent from '../../components/modal/school-select/school-select.vue'
// include dependence
export default {
  name: 'Modal',
  data () {
    return {
      modal: false,
      current: null,
      gold: {
        // 'school-select': SchoolSelectModalComponent
      }
    }
  },
  watch: {
    '$store.state.modal' (modal) {
      if (modal === false) {
        this.modal = false
        this.current = null
      } else {
        this.modal = true
        this.current = this.gold[modal]
      }
    }
  },
  components: {
    // include chunk
    SchoolSelectModalComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./modal.scss";
</style>
