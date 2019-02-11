<template>
  <!-- s 班级详情 -->
  <section class="detail">
    <div class="detail-header">
      <div class="header-title">
        <div class="title-introduction">
          <p class="introduction-name">{{detail.name}}</p>
          <p class="introduction-tip">课程{{courses}}门，学生{{students}}人</p>
        </div>
        <div class="title-adviser">
          <img class="adviser-portrait" src="">
          <div class="adviser-introduce">
            <p class="introduce-name">{{detail.manager.name}}</p>
            <p class="introduce-phone">{{detail.manager.phone}}</p>
          </div>
        </div>
      </div>
      <div class="header-operation">
        <button class="operation-btn">学员报名</button>
        <button class="operation-btn">设置上课提醒时间</button>
        <button class="operation-btn">结业</button>
        <button class="operation-btn">编辑</button>
        <button class="operation-btn">删除</button>
      </div>
    </div>
    <nav class="detail-nav">
      <div class="nav-item" :class="{'selected': current == 'plan'}" @click="selectTable('plan')">课程列表</div>
      <div class="nav-item" :class="{'selected': current == 'enroll'}" @click="selectTable('enroll')">班级学员</div>
    </nav>
    <div class="detail-operation" v-show="current == 'plan'">
      <button class="operation-add" @click="addPlan">
        <i></i>
        <span>添加课程</span>
      </button>
    </div>
    <div class="detail-operation" v-show="current == 'enroll'">
      <button class="operation-add" @click="addEnroll">
        <i></i>
        <span>添加学员</span>
      </button>
    </div>
    <PlanTableComponent v-show="current == 'plan'" :table="plan"></PlanTableComponent>
    <EnrollTableComponent v-show="current == 'enroll'" :table="enroll"></EnrollTableComponent>
  </section>
  <!-- s 班级详情 -->
</template>

<script>
import PlanTableComponent from '../table/plan/plan.vue'
import EnrollTableComponent from '../table/enroll/enroll.vue'
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'ClassDetailComponent',
  data () {
    return {
      detail: {},
      courses: 0,
      students: 0,
      plan: [],
      enroll: [],
      current: 'plan'
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    EnrollTableComponent,
    PlanTableComponent
  },
  created () {
    this.detail = {...Communication.detail}
    this.getPlanList()
    this.getEnrollList()
  },
  methods: {
    addPlan () {
      Display.panel = 'plan-add-plan'
      Communication.panel = this.detail
    },
    addEnroll () {
      Display.panel = 'enroll-add-enroll'
      Communication.panel = this.detail
    },
    getPlanList () {
      Http.send({
        url: 'PlanList',
        data: {
          oid: this.detail.oid
        }
      }).success(data => {
        this.plan = data
        this.courses = data.length
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    getEnrollList () {
      Http.send({
        url: 'EnrollList',
        data: {
          oid: this.detail.oid
        }
      }).success(data => {
        this.enroll = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    selectTable (table) {
      this.current = table
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'PlanList') {
        this.getPlanList()
      } else if (api === 'EnrollList') {
        this.getEnrollList()
      }
      Display.api = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./detail.scss";
</style>
