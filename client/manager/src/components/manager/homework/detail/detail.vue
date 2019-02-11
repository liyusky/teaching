<template>
  <!-- s  -->
  <section class="detail">
    <div class="detail-header">
      <div class="header-title">
        <p class="title-name">
          <span class="name-content">{{detail.name}}</span>
          <span class="name-code">作业编号：{{detail.hid}}</span>
        </p>
        <p class="title-tip">班级：{{detail.curriculumDetail.organization.name}}，课时：{{detail.curriculumDetail.lesson}}</p>
      </div>
      <div class="header-operation">
        <button class="operation-btn" @click="addQuestion">新增题目</button>
        <!-- <button class="operation-btn">编辑</button>
        <button class="operation-btn">删除</button> -->
      </div>
    </div>
    <QuestionComponent :table="table"></QuestionComponent>
  </section>
  <!-- s  -->
</template>

<script>
import QuestionComponent from '../table/question/question.vue'
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'HomeworkDetailComponent',
  data () {
    return {
      detail: {},
      table: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    QuestionComponent
  },
  created () {
    // let data = Communication.detail
    this.detail = {...Communication.detail}
    this.getQuestionList()
  },
  methods: {
    addQuestion () {
      Display.panel = 'question-add-question'
      Communication.panel = Communication.detail
    },
    getQuestionList () {
      Http.send({
        url: 'QuestionList',
        data: {
          hid: this.detail.hid
        }
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'QuestionList') {
        this.getQuestionList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./detail.scss";
</style>
