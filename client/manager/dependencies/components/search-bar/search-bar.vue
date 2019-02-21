<template>
  <!-- s  -->
  <section class="search-bar">
    <input class="search-input" type="text" :placeholder="placeholder" v-model="keywords">
    <button class="search-btn bg-blue" @click="serach">搜索</button>
    <button class="search-btn" @click="refresh" v-if="!notNeedRefresh">刷新</button>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
export default {
  name: 'SearchBarComponent',
  props: ['placeholder', 'notNeedRefresh'],
  data () {
    return {
      keywords: ''
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  methods: {
    serach () {
      this.$emit('SEARCH_EVENT', this.keywords)
    },
    refresh () {
      this.$emit('REFRESH_EVENT', this.keywords)
    }
  },
}
</script>

<style lang="sass" scoped>
@import "./search-bar.scss";
</style>
