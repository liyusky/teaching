<template>
  <!-- s  -->
  <section class="student">
    <HeaderComponent></HeaderComponent>
    <NvaComponent></NvaComponent>
    <router-view/>
    <div class="student-tail"></div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import HeaderComponent from '../../../dependencies/components/header/header.vue'
import NvaComponent from '../../../dependencies/components/nva/nva.vue'
export default {
  name: 'StudentComponent',
  data () {
    return {
      // start datas
      // end datas
    }
  },
  components: {
    HeaderComponent,
    NvaComponent
    // include chunk
  }
}
</script>

<style lang="sass" scoped>
@import "./student.scss";
</style>
