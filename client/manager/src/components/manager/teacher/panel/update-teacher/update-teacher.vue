<template>
  <!-- s  -->
  <section class="update-teacher">
    <div class="teacher-header">
      <p class="header-title">
        <span class="title-main">修改教师信息</span>
        <span class="title-tip">（教师编号 {{uid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="teacher-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-name">姓名：</label>
          <input class="item-input" id="teacher-setting-update-teacher-name" placeholder="2位以上教师真实姓名" type="text" v-model="name" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-phone">手机号：</label>
          <input class="item-input" id="teacher-setting-update-teacher-phone" placeholder="11位教师手机号" type="text" v-model="phone" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-password">密码：</label>
          <input class="item-input" id="teacher-setting-update-teacher-password" placeholder="6到20位，数字，字母，下划线" type="text" v-model="password" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-sex">性别：</label>
          <select class="item-select" id="teacher-setting-update-teacher-sex" v-model="sex" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="1">男</option>
            <option value="0">女</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-role">角色：</label>
          <select class="item-select" id="teacher-setting-update-teacher-role" v-model="role" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="0">学生</option>
            <option value="1">教学老师</option>
            <option value="2">教务老师</option>
            <option value="3">教务主任</option>
            <option value="4">教学主任</option>
            <option value="99">管理员</option>
          </select>
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="教师所属学校，选填" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="teacher-setting-update-teacher-remarks">备注：</label>
          <textarea class="item-textarea close-scrollbar" placeholder="教师备注，选填" id="teacher-setting-update-teacher-remarks" v-model="description" @keyup.enter="confirm" @keyup.esc="cancel"></textarea>
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
import Check from '../../../../../../dependencies/modules/Check.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
// import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'TeacherUpdateTeacherPanelComponent',
  data () {
    return {
      uid: 0,
      upid: 0,
      phone: '',
      name: '',
      sex: '',
      role: 0,
      // college: '',
      // school: 0,
      description: '',
      data: null,
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.data.description = this.data.description
    this.uid = panel.user
    this.upid = panel.upid
    this.phone = panel.phone
    this.name = panel.name
    this.sex = panel.sex
    this.role = panel.role
    // this.college = `${panel.detail.college.name}${panel.detail.college.district || ''}${Dictionary.rank[panel.detail.college.level]}`
    // this.school = panel.school
    this.description = panel.description
  },
  methods: {
    // selectSchool () {
    //   Display.modal = 'school-select'
    // },
    confirm () {
      let data = {
        tid: this.uid
      }
      if (this.data.phone !== this.phone) {
        if (!Check.phone(this.phone)) return
        data.phone = this.phone
      }

      if (this.data.name !== this.name) {
        if (!Check.name(this.name)) return
        data.name = this.name
      }

      if (this.password) {
        if (!Check.password(this.password)) return
        data.password = this.password
      }

      if (this.data.sex !== this.sex) data.sex = this.sex
      if (this.data.role !== this.role) data.role = this.role
      // if (this.school && this.data.school !== this.school) data.school = this.school
      if (this.data.description !== this.description) data.description = this.description

      Http.send({
        url: 'UpdateTeacher',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'TeacherList'
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
    }
  }
  // watch: {
  //   '$store.state.modal' (modal, previous) {
  //     if (previous === 'school-select' && modal === false && Communication.modal) {
  //       this.college = `${Communication.modal.name}${Communication.modal.district}${Dictionary.rank[Communication.modal.level]}`
  //       this.school = {...Communication.modal}.school
  //     }
  //   }
  // }
}
</script>

<style lang="sass" scoped>
@import "./update-teacher.scss";
</style>
