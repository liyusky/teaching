<template>
  <!-- s  -->
  <section class="teacher">
    <div class="teacher-header">
      <p class="header-title">添加教师</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="teacher-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-account">账户：</label>
          <input class="item-input" id="teacher-setting-teacher-account" placeholder="6到30位，数字，字母，下划线" type="text" v-model="account" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-name">姓名：</label>
          <input class="item-input" id="teacher-setting-teacher-name" placeholder="请输入教师真实姓名" type="text" v-model="name" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-phone">手机号：</label>
          <input class="item-input" id="teacher-setting-teacher-phone" placeholder="请输入教师手机号，可不填" type="text" v-model="phone" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="student-setting-teacher-password">密码：</label>
          <input class="item-input" id="student-setting-teacher-password" placeholder="6到20位，数字，字母，下划线" type="text" v-model="password" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-sex">性别：</label>
          <select class="item-select" id="teacher-setting-teacher-sex" v-model="sex" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="1" selected>男</option>
            <option value="0">女</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-role">角色：</label>
          <select class="item-select" id="teacher-setting-teacher-role" v-model="role" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="1" selected>教学老师</option>
            <option value="2">教务老师</option>
            <option value="3">教务主任</option>
            <option value="4">教学主任</option>
            <option value="99">管理员</option>
          </select>
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="教师所属学校，选填" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="teacher-setting-teacher-remarks">备注：</label>
          <textarea class="item-textarea close-scrollbar" placeholder="请填写备注，选填" id="teacher-setting-teacher-remarks" v-model="description" @keyup.enter="confirm" @keyup.esc="cancel"></textarea>
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
  name: 'TeacherAddTeacherPanelComponent',
  data () {
    return {
      phone: '',
      name: '',
      sex: 1,
      role: 1,
      account: '',
      password: '',
      course: '',
      // college: '',
      // school: 0,
      description: '',
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  methods: {
    // selectSchool () {
    //   Display.modal = 'school-select'
    // },
    confirm () {
      if (!Check.account(this.account)) return
      if (!Check.name(this.name)) return
      if (!Check.password(this.password)) return
      let data = {
        account: this.account,
        password: this.password,
        name: this.name,
        sex: this.sex,
        role: this.role
      }
      if (this.phone) {
        if (!Check.phone(this.phone)) return
        data.phone = this.phone
      }
      if (this.description) data.description = this.description
      // if (this.school) data.school = this.school
      Http.send({
        url: 'AddTeacher',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'TeacherList'
      }).fail(data => {
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
      this.sex = 1
      // this.school = 0
      this.role = 1
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
@import "./teacher.scss";
</style>
