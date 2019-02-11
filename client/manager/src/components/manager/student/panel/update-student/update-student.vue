<template>
  <!-- s  -->
  <section class="update-student">
    <div class="student-header">
      <p class="header-title">
        <span class="title-main">修改学员信息</span>
        <span class="title-tip">（学员编号 {{uid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="student-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="student-setting-update-student-name">姓名：</label>
          <input class="item-input" id="student-setting-update-student-name" placeholder="学生真实姓名" type="text" v-model="name" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-update-student-phone">手机号：</label>
          <input class="item-input" id="student-setting-update-student-phone" placeholder="学生手机号，选填" type="text" v-model="phone" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
          <li class="list-item">
          <label class="item-label" for="student-setting-update-student-password">密码：</label>
          <input class="item-input" id="student-setting-update-student-password" placeholder="登录密码，非空字符串" type="text" v-model="password" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-update-student-sex">性别：</label>
          <select class="item-select" id="student-setting-update-student-sex" v-model="sex" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="1">男</option>
            <option value="0">女</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-update-student-role">角色：</label>
          <select class="item-select" id="student-setting-update-student-role" v-model="role" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="0">学生</option>
            <option value="1">教学老师</option>
            <option value="2">教务老师</option>
            <option value="3">教务主任</option>
            <option value="4">教学主任</option>
            <option value="99">管理员</option>
          </select>
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="student-setting-update-student-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学生所属学校" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="student-setting-update-student-grade">年级：</label>
          <select class="item-select" id="student-setting-update-student-grade" v-model="grade" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="0">未知</option>
            <option value="1">小一</option>
            <option value="2">小二</option>
            <option value="3">小三</option>
            <option value="4">小四</option>
            <option value="5">小五</option>
            <option value="6">小六</option>
            <option value="7">初一</option>
            <option value="8">初二</option>
            <option value="9">初三</option>
            <option value="10">高一</option>
            <option value="11">高二</option>
            <option value="12">高三</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-update-student-remarks">备注：</label>
          <textarea class="item-textarea close-scrollbar" placeholder="学生备注，选填" id="student-setting-update-student-remarks" v-model="description" @keyup.enter="confirm" @keyup.esc="cancel"></textarea>
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
  name: 'StudentUpdateStudentPanelComponent',
  data () {
    return {
      uid: 0,
      upid: 0,
      phone: '',
      name: '',
      password: '',
      sex: '',
      role: 0,
      // school: 0,
      // college: '',
      grade: 0,
      description: '',
      data: null,
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  created () {
    console.log(Communication.panel)
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.data.description = this.data.description
    this.uid = panel.user
    this.upid = panel.upid
    this.phone = panel.phone
    this.name = panel.name
    this.sex = panel.sex
    this.role = panel.role
    // this.college = this.getCollege(panel.detail.college)
    // this.school = panel.school
    this.grade = panel.grade
    this.description = panel.description
  },
  methods: {
    // getCollege (college) {
    //   if (college) {
    //     return `${college.name}${college.district && college.district !== 'null' ? college.district : ''}${Dictionary.rank[college.level]}`
    //   } else {
    //     return '未设置'
    //   }
    // },
    // selectSchool () {
    //   Display.modal = 'school-select'
    // },
    confirm () {
      console.log(Communication.panel)
      let data = {
        sid: this.uid
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
      if (this.data.grade !== this.grade) data.grade = this.grade
      if (this.data.description !== this.description && this.description) data.description = this.description

      Http.send({
        url: 'UpdateStudent',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'StudentList'
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
@import "./update-student.scss";
</style>
