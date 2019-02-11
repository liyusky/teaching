<template>
  <!-- s  -->
  <section class="update-user">
    <div class="user-header">
      <p class="header-title">
        <span class="title-name">修改用户信息</span>
      </p>
      <div class="header-close" v-show="allow" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="user-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="account-setting-update-name">姓名：</label>
          <input class="item-input" id="account-setting-update-name" placeholder="请填入真实姓名" type="text" v-model="name" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="account-setting-update-phone">手机号：</label>
          <input class="item-input" id="account-setting-update-phone" type="phone" v-model="phone" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="account-setting-update-age">年龄：</label>
          <input class="item-input" id="account-setting-update-age" placeholder="请填入真实年龄" type="text" v-model="age" @keyup.enter="confirm" @keyup.esc="cancel">
        </li>
        <li class="list-item">
          <label class="item-label" for="account-setting-update-sex">性别：</label>
          <select class="item-select" id="account-setting-update-sex" v-model="sex" @keyup.enter="confirm" @keyup.esc="cancel">
            <option value="1">男</option>
            <option value="0">女</option>
          </select>
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="account-setting-update-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学校" @click="selectSchool" @keyup.enter="confirm" @keyup.esc="cancel">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="account-setting-update-remarks">备注：</label>
          <textarea class="item-textarea close-scrollbar" id="account-setting-update-remarks" placeholder="请填入备注，选填" v-model="description" @keyup.enter="confirm" @keyup.esc="cancel"></textarea>
        </li>
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
        <button class="btns-cancel" v-show="allow" @click="cancel">取消</button>
      </section>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../../../../dependencies/modules/Account.class.js'
import Check from '../../../../../dependencies/modules/Check.class.js'
// import Communication from '../../../../../dependencies/modules/Communication.class.js'
// import Dictionary from '../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'UserUpdateUserPanelComponent',
  data () {
    return {
      allow: Account.name,
      uid: Account.uid,
      sex: Account.sex,
      name: Account.name,
      password: '',
      age: Account.age,
      // college: `${Account.college.name}${Account.college.district || ''}${Dictionary.rank[Account.college.level]}`,
      // school: Account.school,
      description: Account.description,
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
      let data = {
        uid: this.uid
      }

      if (this.name !== Account.name) {
        if (!Check.name(this.name)) return
        data.name = this.name
      }

      // if (this.phone) {
      //   if (!Check.phone(this.phone)) return
      //   data.phone = this.phone
      // }

      if (this.sex !== Account.sex) data.sex = this.sex
      if (this.age !== Account.age) {
        if (!Check.age(this.age)) return
        data.age = this.age
      }
      // if (this.school && Account.school !== this.school) data.school = this.school
      if (this.description !== Account.description) data.description = this.description

      Http.send({
        url: 'UpdateAccount',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Account.info = data
        alert('个人信息更新成功')
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      // if (Account.name && Account.phone) Display.panel = false
      if (Account.name) Display.panel = false
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
@import "./update-user.scss";
</style>
