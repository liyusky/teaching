<template>
  <!-- s  -->
  <section class="update-enroll">
    <div class="enroll-header">
      <p class="header-title">修改学员信息</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="enroll-operation">
      <ul class="operation-setting-list">
        <!-- <li class="list-item">
          <label class="item-label" for="enroll-setting-update-class">班级：</label>
          <input class="item-input" id="enroll-setting-update-class" type="text" readonly="readonly" v-model="organization" placeholder="请点击选择课程" @click="selectClass">
        </li> -->
        <!-- <li class="list-item">
          <label class="item-label" for="enroll-setting-update-course">当前课程：</label>
          <input class="item-input" id="enroll-setting-update-course" type="text" readonly="readonly" v-model="course" placeholder="请点击选择课程" @click="selectCourse">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="enroll-setting-update-student">学员：</label>
          <input class="item-input" id="enroll-setting-update-student" type="text" readonly="readonly" v-model="student" placeholder="请点击选择学员" @click="selectStudent">
        </li>
        <li class="list-item">
          <label class="item-label" for="enroll-setting-update-status">状态：</label>
          <select class="item-select" id="enroll-setting-update-status" v-model="status">
            <option value="0">未决定</option>
            <option value="1">学习中</option>
            <option value="2">结业</option>
            <option value="3">肄业</option>
          </select>
        </li>
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
        <button class="btns-cancel" @click="cancel">取消</button>
      </section>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'EnrollUpdateEnrollPanelComponent',
  data () {
    return {
      oid: '',
      cid: '',
      sid: '',
      eid: '',
      studentid: 0,
      student: '',
      organization: '',
      course: '',
      status: 0,
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.oid = panel.oid
    this.sid = panel.sid
    this.eid = panel.eid
    this.status = panel.status
    this.organization = panel.organization.name
    this.student = `${panel.studentDetail.name}（${panel.studentDetail.phone}）`
  },
  methods: {
    selectStudent () {
      Display.modal = 'student-select'
    },
    selectCourse () {
      Display.modal = 'course-select'
    },
    selectClass () {
      Display.modal = 'class-select'
    },
    confirm () {
      let data = {eid: this.eid}

      if (this.data.oid !== this.oid) {
        data.oid = this.oid
        data.cls = this.oid
      }
      if (this.data.sid !== this.sid) {
        data.student = this.sid
      }

      if (this.data.status !== this.status) {
        data.status = this.status
      }
      Http.send({
        url: 'UpdateEnroll',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'EnrollList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
      Communication.modal = false
      this.clear()
    },
    clear () {
      this.cid = ''
      this.sid = ''
      this.course = ''
      this.student = ''
      this.organization = ''
      this.status = 0
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'student-select' && modal === false && Communication.modal) {
        this.student = `${Communication.modal.detail.realname}（${Communication.modal.phone}）`
        this.sid = {...Communication.modal}.user
      } else if (previous === 'course-select' && modal === false && Communication.modal) {
        this.course = `${Communication.modal.name}（${Dictionary.language[Communication.modal.language]}，${Dictionary.rank[Communication.modal.grade]}）`
        this.cid = {...Communication.modal}.cid
      } else if (previous === 'class-select' && modal === false && Communication.modal) {
        this.organization = `${Communication.modal.name}（${Communication.modal.manager.name} ${Communication.modal.manager.phone}）`
        this.oid = {...Communication.modal}.oid
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./update-enroll.scss";
</style>
