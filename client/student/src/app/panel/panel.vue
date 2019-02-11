<template>
  <!-- s  -->
  <section class="panel" id="panel" v-show="panel">
    <component :is="current"></component>
  </section>
  <!-- s  -->
</template>

<script>
// 班级
import UserUpdateUserPanelComponent from '../../components/panel/user/update-user/update-user.vue'
// include dependence
export default {
  name: 'Panel',
  data () {
    return {
      panel: false,
      current: null,
      gold: {
        'user-update-user': UserUpdateUserPanelComponent
      }
      // start datas
      // end datas
    }
  },
  watch: {
    '$store.state.panel' (panel) {
      if (panel === false) {
        this.panel = false
        this.current = null
      } else {
        this.panel = true
        this.current = this.gold[panel]
      }
    }
  },
  components: {
    // include chunk
    UserUpdateUserPanelComponent
  }
}
</script>

<style lang="sass" scoped>
@import "./panel.scss";
</style>
