<template>
  <!-- s  -->
  <section class="student-select">
    <div class="select-header">
      <p class="header-title">选择学员</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="content-list">
        <li class="list-item fl" v-for="(item, index) in students" :key="index" @click="select(item)">
          <div class="item-warp">
            <img class="warp-portrait" src="">
            <p class="warp-name">{{item.name}}</p>
            <p class="warp-phone">{{item.phone}}</p>
            <!-- <p class="warp-school">{{getCollege(item.detail)}}</p> -->
          </div>
        </li>
      </ul>
    </div>
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
  name: 'StudentSelectModalComponent',
  data () {
    return {
      students: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getStudentList()
  },
  methods: {
    // getCollege (detail) {
    //   if ('college' in detail) {
    //     return `${detail.college.name}${detail.college.district && detail.college.district !== 'null' ? detail.college.district : ''}${Dictionary.rank[detail.college.level]}`
    //   } else {
    //     return '未设置'
    //   }
    // },
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getStudentList () {
      Http.send({
        url: 'StudentList'
      }).success(data => {
        this.students = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./student-select.scss";
</style>
