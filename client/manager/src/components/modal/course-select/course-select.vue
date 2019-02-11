<template>
  <!-- s  -->
  <section class="course-select">
    <div class="select-header">
      <p class="header-title">选择课程</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="select-list">
        <li class="list-item fl" v-for="(item, index) in course" :key="index" @click="select(item)">
          <div class="item-wrap">
            <img class="wrap-portrait" src="">
            <div class="wrap-message">
              <p class="message-name">{{item.name}}</p>
              <p class="message-tip">{{language[item.language]}}，{{rank[item.grade]}}</p>
            </div>
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
import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'

export default {
  name: 'CourseSelectModalComponent',
  data () {
    return {
      language: Dictionary.language,
      rank: Dictionary.rank,
      course: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getCourseList()
  },
  methods: {
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getCourseList () {
      Http.send({
        url: 'CourseList'
      }).success(data => {
        this.course = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./course-select.scss";
</style>
