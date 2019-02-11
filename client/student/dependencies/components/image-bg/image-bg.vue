<template>
  <!-- s  -->
  <section class="image-bg">
    <img :src="imageBg">
  </section>
  <!-- s  -->
</template>

<script>
export default {
  name: 'ImageBgComponent',
  props: ['imageBg']
}
</script>

<style lang="sass" scoped>
@import "./image-bg.scss";
</style>
