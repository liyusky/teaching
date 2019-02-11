<template>
  <!-- s  -->
  <section class="empower">
    <ImageBgComponent class="empower-bg" :imageBg="imageBg"></ImageBgComponent>
    <div class="empower-area" :class="status">
      <div class="area-logo">
        <img class="logo-image" src="../../assets/logo.png">
        <p class="logo-tip">发现编程的乐趣</p>
      </div>
      <ul class="area-input-list">
        <li class="list-item border-1">
          <input class="item-input" v-model="phone" type="text" maxlength="11" placeholder="请输入账号" @keyup.enter="submit">
        </li>
        <li class="list-item border-1" v-show="!smsMode">
          <input class="item-input" v-model="password" type="password" maxlength="20" placeholder="请输入密码" @keyup.enter="submit">
        </li>
        <li class="list-item border-1">
          <input class="item-input" v-model="imageCode" type="text" maxlength="4" placeholder="请输入图形验证码" @keyup.enter="submit">
          <img class="item-image" :src="codeImage" @click="getCodeImage">
        </li>
        <li class="list-item border-1" v-show="smsMode || status != 'login'">
          <input class="item-input" v-model="smsCode" type="text" maxlength="6" placeholder="请输入短信验证码" @keyup.enter="submit">
          <button class="item-btn" :disabled='smsDisabled' @click="sendSMSCaptcha">{{sendSMSBtnText}}</button>
        </li>
      </ul>
      <div class="area-operation">
        <button class="operation-btn btn-left" @click="switchStatus(true)">
          <div>{{leftBtn}}</div>
        </button>
        <button class="operation-btn" v-show="status != 'register'" @click="switchStatus(false)">
          <div>{{rightBtn}}</div>
        </button>
      </div>
      <button :disabled='submitDisabled' class="area-btn" @click="submit">
        <div>{{submitBtn}}</div>
      </button>
      <div class="area-mode" v-show="status == 'login'">
        <button @click="changLoginMode">{{loginMode}}</button>
      </div>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../../dependencies/modules/Account.class.js'
import Check from '../../../dependencies/modules/Check.class.js'
import Display from '../../../dependencies/modules/Display.class.js'
import Http from '../../../dependencies/modules/Http.class.js'
import Router from '../../../dependencies/modules/Router.class.js'
import ImageBgComponent from '../../../dependencies/components/image-bg/image-bg.vue'
import InputsComponent from '../../../dependencies/components/inputs/inputs.vue'
export default {
  name: 'LoginComponent',
  data () {
    return {
      sms: {},
      scene: 0,
      status: 'login',
      smsMode: false,
      leftBtn: '注册',
      rightBtn: '忘记密码？',
      submitBtn: '登录',
      loginMode: '账号手机验证码登录',
      phone: '',
      password: '',
      codeImage: '',
      imageCode: '',
      smsCode: '',
      smsDisabled: false,
      submitDisabled: false,
      sendSMSBtnText: '获取短信验证码',
      // start datas
      imageBg: '../../../static/images/bg.jpg'
      // end datas
    }
  },
  components: {
    ImageBgComponent,
    InputsComponent
    // include components
  },
  created () {
    this.clearStorage()
    this.getCodeImage()
  },
  methods: {
    getCodeImage () {
      this.codeImage = `${window.baseUrl}/common/image-code?time=${new Date()}`
    },
    switchStatus (state) {
      switch (this.status) {
        case 'login':
          if (state) {
            this.scene = 1
            this.status = 'register'
            this.leftBtn = '登录'
            this.submitBtn = '注册'
          } else {
            this.scene = 2
            this.status = 'forget-password'
            this.leftBtn = '登录'
            this.rightBtn = '注册'
            this.submitBtn = '修改密码'
          }
          break
        case 'register':
          this.scene = 0
          this.status = 'login'
          this.leftBtn = '注册'
          this.rightBtn = '忘记密码？'
          this.submitBtn = '登录'
          break
        case 'forget-password':
          if (state) {
            this.scene = 0
            this.status = 'login'
            this.leftBtn = '注册'
            this.rightBtn = '忘记密码？'
            this.submitBtn = '登录'
          } else {
            this.scene = 1
            this.status = 'register'
            this.leftBtn = '登录'
            this.submitBtn = '注册'
          }
          break
      }
    },
    changLoginMode () {
      this.smsMode = !this.smsMode
      this.loginMode = this.smsMode ? '账号密码登录' : '账号手机验证码登录'
    },
    sendSMSCaptcha () {
      if (!Check.phone(this.phone)) return
      if (!Check.imageCode(this.imageCode)) return
      this.waitOneMinute()
      Http.send({
        url: 'SMSCaptcha',
        data: {
          phone: this.phone,
          imageCode: this.imageCode,
          scene: this.scene
        }
      }).success(data => {
        alert('短信验证码已发送')
      }).fail(data => {
        alert('短信验证码发送失败')
        console.log(data)
      })
    },
    waitOneMinute () {
      this.smsDisabled = true
      this.sendSMSBtnText = '60秒后重发'
      let time = 60
      let animation = setInterval(() => {
        time--
        if (time > 0) {
          this.sendSMSBtnText = `${time}秒后重发`
        } else {
          this.sendSMSBtnText = '获取短信验证码'
          clearInterval(animation)
          this.smsDisabled = false
        }
      }, 1000)
    },
    submit () {
      if (this.status === 'login' && !this.smsMode) this.loginByPassword()
      if (this.status === 'login' && this.smsMode) this.loginBySMS()
      if (this.status === 'register') this.register()
      if (this.status === 'forget-password') this.forgetPassword()
    },
    loginByPassword () {
      if (!Check.account(this.phone)) return
      if (!Check.password(this.password)) return
      if (!Check.imageCode(this.imageCode)) return
      this.submitDisabled = true
      Http.send({
        url: 'LoginByPassword',
        data: {
          phone: this.phone,
          password: this.password,
          imageCode: this.imageCode
        }
      }).success(data => {
        Account.info = data
        Router.push('student')
        // if (!data.name || !data.school) Display.panel = 'user-update-user'
        if (!data.name) Display.panel = 'user-update-user'
      }).fail(data => {
      }).default(() => {
        this.getCodeImage()
        this.submitDisabled = false
      })
    },
    loginBySMS () {
      if (!Check.phone(this.phone)) return
      if (!Check.smsCode(this.smsCode)) return
      this.submitDisabled = true
      Http.send({
        url: 'LoginBySMS',
        data: {
          phone: this.phone,
          smsCode: this.smsCode
        }
      }).success(data => {
        Account.info = data
        Router.push('student')
        // if (!data.name || !data.school) {
        //   Display.panel = 'user-update-user'
        // }
        if (!data.name) Display.panel = 'user-update-user'
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.getCodeImage()
        this.submitDisabled = false
      })
    },
    register () {
      if (!Check.phone(this.phone)) return
      if (!Check.password(this.password)) return
      if (!Check.smsCode(this.smsCode)) return
      this.submitDisabled = true
      Http.send({
        url: 'Register',
        data: {
          account: this.phone,
          password: this.password,
          smsCode: this.smsCode
        }
      }).success(data => {
        Account.info = data
        Router.push('student')
        // if (!data.name || !data.school) {
        //   Display.panel = 'user-update-user'
        // }
        if (!data.name) Display.panel = 'user-update-user'
        alert('注册成功，您可以双击右上角修改个人信息')
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.getCodeImage()
        this.submitDisabled = false
      })
    },
    forgetPassword () {
      if (!Check.phone(this.phone)) return
      if (!Check.password(this.password)) return
      if (!Check.smsCode(this.smsCode)) return
      this.submitDisabled = true
      Http.send({
        url: 'ForgetPassword',
        data: {
          phone: this.phone,
          password: this.password,
          smsCode: this.smsCode
        }
      }).success(data => {
        this.switchStatus(true)
        alert('密码修改成功')
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.getCodeImage()
        this.submitDisabled = false
      })
    },
    loginByPasswordAfterToken () {
      this.submitDisabled = true
    },
    clearStorage () {
      this.$store.commit('account', {})
      this.$store.commit('origin', null)
      this.$store.commit('modal', false)
      this.$store.commit('panel', false)
      this.$store.commit('detail', false)
      this.$store.commit('api', false)
      this.$store.commit('tip', false)
      this.$store.commit('nav', [])
      this.$store.commit('content', false)
      this.$store.commit('communication', {})
      localStorage.clear()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./login.scss";
</style>
