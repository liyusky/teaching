<template>
  <!-- s 学员报名 -->
  <section class="enroll">
    <div class="enroll-header">
      <p class="header-title">学员报名</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="enroll-operation">
      <ul class="operation-setting-list">
        <!-- <li class="list-item">
          <label class="item-label" for="plan-setting-add-name">当前课程：</label>
          <input class="item-input" id="plan-setting-add-manager" type="text" readonly="readonly" v-model="course" placeholder="请点击选择课程" @click="selectCourse">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="plan-setting-add-teacher">学员：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="student" placeholder="请点击选择学员" @click="selectStudent">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="plan-setting-add-school">状态：</label>
          <select class="item-select" id="plan-setting-add-school" v-model="status">
            <option value="0" selected>未决定</option>
            <option value="1">学习中</option>
            <option value="2">结业</option>
            <option value="3">肄业</option>
          </select>
        </li> -->
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
        <button class="btns-cancel" @click="cancel">取消</button>
      </section>
    </div>
  </section>
  <!-- s 学员报名 -->
</template>

<script>
// include dependence
// import Account from '../../../../../../dependencies/modules/Account.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'EnrollAddEnrollPanelComponent',
  data () {
    return {
      oid: '',
      cid: '',
      sid: '',
      status: 0,
      course: '',
      student: '',
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.oid = Communication.panel.oid
    let panel = {...Communication.panel}
    panel.page = 'add-enroll'
    Communication.panel = panel
  },
  methods: {
    selectStudent () {
      Display.modal = 'student-select'
    },
    selectCourse () {
      Display.modal = 'course-select'
    },
    confirm () {
      Http.send({
        url: 'AddEnroll',
        data: {
          oid: this.oid,
          student: JSON.stringify(this.sid)
        }
      }).success(data => {
        Display.api = 'EnrollList'
        let message = `${data.success}条数据更新成功，${data.fail}条数据更新失败，${data.used}条数据本身已存在，${data.error}条数据发生错误。`
        alert(message)
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        this.cancel()
      })
    },
    cancel () {
      Display.panel = false
      Communication.modal = false
      this.clear()
    },
    clear () {
      this.oid = ''
      this.cid = ''
      this.sid = ''
      this.course = ''
      this.student = ''
      this.status = 1
      this.confirmDisabled = false
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'student-select' && modal === false && Communication.modal) {
        let [student, sid] = ['', []]
        Communication.modal.forEach(item => {
          student += `${item.detail.realname}（${item.phone}），`
          sid.push(item.user)
        })
        this.student = student
        this.sid = sid
      } else if (previous === 'course-select' && modal === false && Communication.modal) {
        this.course = `${Communication.modal.name}（${Dictionary.language[Communication.modal.language]}，${Dictionary.rank[Communication.modal.grade]} ）`
        this.cid = {...Communication.modal}.cid
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./enroll.scss";
</style>
