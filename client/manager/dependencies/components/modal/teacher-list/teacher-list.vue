<template>
  <!-- s  -->
  <section class="teacher-list">
    <h3 class="list-title">选择教师</h3>
    <ul class="list-content">
      <li class="content-item fl" v-for="(item, index) in teachers" :key="index">
        <div class="item-warp">
          <img class="warp-portrait" src="">
          <p class="warp-name">{{item.name}}</p>
          <p class="warp-phone">{{item.teacher}}</p>
          <p class="warp-school">{{item.school}}</p>
        </div>
      </li>
    </ul>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
export default {
  name: 'TeacherListComponent',
  data () {
    return {
      // start datas
      // end datas
    }
  },
  created () {},
  components: {
    // include chunk
  },
  methods: {
    getTeacherList () {
      
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./teacher-list.scss";
</style>
