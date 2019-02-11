<template>
  <!-- s  -->
  <section class="tip" id="tip" v-show="tip">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
import SchoolAddSchoolPanelComponent from '../../components/manager/school/panel/add-school/add-school.vue'
export default {
  name: 'Tip',
  data () {
    return {
      tip: false,
      current: null,
      gold: {
        // 'school-add-school': SchoolAddSchoolPanelComponent
      }
    }
  },
  watch: {
    '$store.state.tip' (tip) {
      if (tip === false) {
        this.tip = false
        this.current = null
      } else {
        this.tip = true
        this.current = this.gold[tip]
      }
    }
  },
  components: {
    SchoolAddSchoolPanelComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./tip.scss";
</style>
