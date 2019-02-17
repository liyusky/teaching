<template>
  <!-- s  -->
  <section class="detail">
    <div class="detail-header">
      <div class="header-title">
        <p class="title-name">
          <span class="name-content">{{name}}</span>
          <span class="name-code">班级编号：{{cid}}</span>
        </p>
        <p class="title-tip">创建人：{{creater.name}}（{{creater.phone}}）, 共{{count}}课时，120分钟/课时</p>
      </div>
      <div class="header-operation" v-if="setPermission()">
        <button class="operation-btn" @click="addLesson">新增课时</button>
        <!-- <button class="operation-btn">编辑</button>
        <button class="operation-btn">删除</button> -->
      </div>
    </div>
    <LessonTableComponent :table="table"></LessonTableComponent>
  </section>
  <!-- s  -->
</template>

<script>
import LessonTableComponent from '../table/lesson/lesson.vue'
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'
import Account from '../../../../../dependencies/modules/Account.class.js'

export default {
  name: 'CourseDetailComponent',
  data () {
    return {
      cid: 0,
      name: '',
      creator: {},
      count: 0,
      table: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    LessonTableComponent
  },
  created () {
    this.name = Communication.detail.name
    this.cid = Communication.detail.cid
    this.creater = Communication.detail.creater
    this.getLessonList()
  },
  methods: {
    setPermission () {
      let show = true
      if (Account.role < 99) show = false
      return show
    },
    addLesson () {
      Display.panel = 'lesson-add-lesson'
      Communication.panel = Communication.detail
    },
    getLessonList () {
      Http.send({
        url: 'LessonList',
        data: {
          cid: this.cid
        }
      }).success(data => {
        this.table = data
        this.count = data.length
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'LessonList') {
        this.getLessonList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./detail.scss";
</style>
