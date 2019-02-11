<template>
  <!-- s  -->
  <TemplateComponent>
    <router-view/>
  </TemplateComponent>
  <!-- s  -->
</template>

<script>
// include dependence
import TemplateComponent from '../../../dependencies/components/template/template.vue'
export default {
  name: 'ManagerComponent',
  data () {
    return {
      // start datas
      template: true
      // end datas
    }
  },
  components: {
    TemplateComponent
    // include chunk
  }
}
</script>

<style lang="sass" scoped>
@import "./manager.scss";
</style>
