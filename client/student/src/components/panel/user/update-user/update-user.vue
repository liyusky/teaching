<template>
  <!-- s  -->
  <section class="update-user">
    <div class="user-header">
      <p class="header-title">
        <span class="title-name">更新用户信息</span>
      </p>
    </div>
    <div class="user-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="account-setting-update-name">姓名：</label>
          <input class="item-input" id="account-setting-update-name" type="text" v-model="name">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="account-setting-update-password">密码：</label>
          <input class="item-input" id="account-setting-update-password" type="password" v-model="password">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="account-setting-update-age">年纪：</label>
          <input class="item-input" id="account-setting-update-age" type="text" v-model="age">
        </li>
        <li class="list-item">
          <label class="item-label" for="account-setting-update-sex">性别：</label>
          <select class="item-select" id="account-setting-update-sex" v-model="sex">
            <option value="1">男</option>
            <option value="0">女</option>
          </select>
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="account-setting-update-school">学校：</label>
          <input class="item-input" id="plan-setting-add-teacher" type="text" readonly="readonly" v-model="college" placeholder="请点击选择学校" @click="selectSchool">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="account-setting-update-remarks">备注：</label>
          <textarea class="item-textarea close-scrollbar" id="account-setting-update-remarks" v-model="description"></textarea>
        </li>
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
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
      uid: Account.uid,
      sex: Account.sex,
      name: Account.name,
      password: '',
      age: Account.age,
      // college: this.getCollege(Account.college),
      // school: Account.school ? Account.school : 0,
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

      if (this.sex !== Account.sex) data.sex = this.sex
      if (this.age !== Account.age && this.age) data.age = this.age
      // if (this.school !== Account.school && this.school) data.school = this.school
      if (this.description !== Account.description && this.description) data.description = this.description

      this.confirmDisabled = true
      Http.send({
        url: 'UpdateAccount',
        data: data
      }).before(() => {
      }).success(data => {
        Account.info = data
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
  //       this.college = `${Communication.modal.name}${Communication.modal.district ? Communication.modal.district : ''}${Dictionary.rank[Communication.modal.level]}`
  //       console.log(this.college)
  //       this.school = {...Communication.modal}.school
  //     }
  //   }
  // }
}
</script>

<style lang="sass" scoped>
@import "./update-user.scss";
</style>
