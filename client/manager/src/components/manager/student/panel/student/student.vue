<template>
  <!-- s  -->
  <section class="student">
    <div class="student-header">
      <p class="header-title">添加学员</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="student-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="student-setting-student-account">账户：</label>
          <input class="item-input" id="student-setting-student-account" placeholder="6-30位账户名，数字，字母，下划线" type="text" v-model="account" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-student-name">姓名：</label>
          <input class="item-input" id="student-setting-student-name" placeholder="学生真实姓名" type="text" v-model="name" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-student-phone">手机号：</label>
          <input class="item-input" id="student-setting-student-phone" placeholder="学生手机号，选填" type="text" v-model="phone" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-student-password">密码：</label>
          <input class="item-input" id="student-setting-student-password" placeholder="请输入密码，非空字符串" type="text" v-model="password" @keyup.enter="confirm"  @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-student-sex">性别：</label>
          <select class="item-select" id="student-setting-student-sex" v-model="sex" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="1" selected>男</option>
            <option value="0">女</option>
          </select>
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="student-setting-student-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学生所属学校" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="student-setting-student-grade">年级：</label>
          <select class="item-select" id="student-setting-student-grade" v-model="grade" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="0" selected>未知</option>
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
          <label class="item-label" for="student-setting-student-remarks">备注：</label>
          <textarea class="item-textarea close-scrollbar" id="student-setting-student-remarks" placeholder="学生备注，选填" v-model="description" @keyup.enter="confirm" @keyup.esc="cancel"></textarea>
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
// import Account from '../../../../../../dependencies/modules/Account.class.js'
import Check from '../../../../../../dependencies/modules/Check.class.js'
// import Communication from '../../../../../../dependencies/modules/Communication.class.js'
// import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'StudentAddStudentPanelComponent',
  data () {
    return {
      phone: '',
      name: '',
      account: '',
      password: '',
      sex: 1,
      role: 0,
      // school: 0,
      // college: '',
      grade: 0,
      description: '',
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  methods: {
    // selectSchool () {
    //   Display.modal = 'school-select'
    // },
    confirm () {
      if (!Check.account(this.account)) return
      if (!Check.password(this.password)) return
      if (!Check.name(this.name)) return
      let data = {
        account: this.account,
        password: this.password,
        name: this.name,
        sex: this.sex,
        role: 0,
        grade: this.grade
      }
      if (this.phone) {
        if (!Check.phone(this.phone)) return
        data.phone = this.phone
      }
      if (this.description) data.description = this.description
      // if (this.school) data.school = this.school
      Http.send({
        url: 'AddStudent',
        data: data
      }).success(data => {
        Display.api = 'StudentList'
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.confirmDisabled = false
        this.cancel()
      })
    },
    cancel () {
      Display.panel = false
      this.clear()
    },
    clear () {
      this.phone = ''
      this.name = ''
      this.password = ''
      this.sex = ''
      // this.school = 0
      this.grade = 0
      this.role = 0
      this.description = ''
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
@import "./student.scss";
</style>
