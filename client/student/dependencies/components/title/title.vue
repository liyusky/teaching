<template>
  <!-- s  -->
  <section class="title">
    <i></i>
    <span>{{title}}</span>
  </section>
  <!-- s  -->
</template>

<script>
export default {
  name: 'TitleComponent',
  props: ['title'],
  data () {
    return {
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./title.scss";
</style>
