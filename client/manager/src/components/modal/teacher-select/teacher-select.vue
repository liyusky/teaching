<template>
  <!-- s  -->
  <section class="teacher-select">
    <div class="select-header">
      <p class="header-title">选择教师</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <ul class="select-list">
      <li class="list-item fl" v-for="(item, index) in teachers" :key="index" @click="select(item)">
        <div class="item-warp">
          <img class="warp-portrait" src="">
          <p class="warp-name">{{item.detail.realname}}</p>
          <p class="warp-phone">{{item.phone}}</p>
          <!-- <p class="warp-school">{{getCollege(item.detail)}}</p> -->
        </div>
      </li>
    </ul>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
// import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'

export default {
  name: 'TeacherSelectModalComponent',
  data () {
    return {
      teachers: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getTeacherList()
  },
  methods: {
    // getCollege (detail) {
    //   if ('college' in detail) {
    //     return `${detail.college.name}${detail.college.district && detail.college.district !== 'null' ? detail.college.district : ''}${Dictionary.rank[detail.college.level]}`
    //   } else {
    //     return '未知学校'
    //   }
    // },
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getTeacherList () {
      Http.send({
        url: 'TeacherList'
      }).success(data => {
        this.teachers = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./teacher-select.scss";
</style>
