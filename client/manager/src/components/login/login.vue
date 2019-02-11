<template>
  <!-- s  -->
  <section class="login">
    <div class="login-background">
      <img src="../../../static/images/bg.jpg">
    </div>
    <div class="login-area">
      <div class="area-logo">
        <img class="logo-image" src="../../../static/images/logo.png">
        <p class="logo-tip">发现编程的乐趣</p>
      </div>
      <ul class="area-input-list">
        <li class="list-item border-1">
          <input class="item-input" v-model="phone" type="text" maxlength="11" placeholder="请输入手机号" @keyup.enter="submit" @keyup.ctrl.enter="sendSMSCaptcha">
        </li>
        <li class="list-item border-1" v-show="!mode">
          <input class="item-input" v-model="password" type="password" maxlength="20" placeholder="请输入密码" @keyup.enter="submit">
        </li>
        <li class="list-item border-1">
          <input class="item-input" v-model="imageCode" type="text" maxlength="4" placeholder="请输入图形验证码" @keyup.enter="submit" @keyup.ctrl.enter="sendSMSCaptcha">
          <img class="item-image" :src="codeImage" @click="getCodeImage">
        </li>
        <li class="list-item border-1" v-show="mode">
          <input class="item-input" v-model="smsCode" type="text" maxlength="6" placeholder="请输入短信验证码" @keyup.enter="submit" @keyup.ctrl.enter="sendSMSCaptcha">
          <button class="item-btn" :disabled='smsDisabled' @click="sendSMSCaptcha">{{sendSMSBtnText}}</button>
        </li>
      </ul>
      <button :disabled='submitDisabled' class="area-btn" @click="submit">
        <div>登录</div>
      </button>
      <div class="area-mode">
        <button @click="changMode">{{modeBtnText}}</button>
      </div>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../../dependencies/modules/Account.class.js'
import Check from '../../../dependencies/modules/Check.class.js'
import Dictionary from '../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../dependencies/modules/Display.class.js'
import Http from '../../../dependencies/modules/Http.class.js'
import Router from '../../../dependencies/modules/Router.class.js'

export default {
  name: 'LoginComponent',
  data () {
    return {
      mode: false,
      phone: '',
      password: '',
      imageCode: '',
      smsCode: '',
      modeBtnText: '手机验证码登录',
      sendSMSBtnText: '获取验证码',
      codeImage: `${Dictionary.baseUrl}/common/image-code?time=${new Date()}`,
      submitDisabled: false,
      smsDisabled: false
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.clearStorage()
    this.getCodeImage()
  },
  mounted () {
    this.getCodeImage()
  },
  methods: {
    changMode () {
      this.mode = !this.mode
      this.modeBtnText = this.mode ? '密码登录' : '手机验证码登录'
    },
    submit () {
      this.mode ? this.loginBySMS() : this.loginByPassword()
      this.getCodeImage()
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
        if (Account.role) {
          Router.push('manager-class')
          // if (!data.name || !data.phone) {
          //   Display.panel = 'user-update-user'
          // }
          if (!data.name) {
            Display.panel = 'user-update-user'
          }
        } else {
          alert('您不是教师，无法登陆')
        }
      }).fail(data => {
      }).default(() => {
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
        if (Account.role) {
          Router.push('manager-class')
          // if (!data.name || !data.school) {
          //   Display.panel = 'user-update-user'
          // }
          if (!data.name) {
            Display.panel = 'user-update-user'
          }
        } else {
          alert('您不是教师，无法登陆')
        }
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.submitDisabled = false
      })
    },
    getCodeImage () {
      this.codeImage = `${window.baseUrl}/common/image-code?time=${new Date()}`
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
          scene: 0
        }
      }).success(data => {
        alert('短信验证码发送成功')
      }).fail(data => {
      }).default(() => {
        this.getCodeImage()
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
    clearStorage () {
      this.$store.commit('account', {})
      this.$store.commit('origin', null)
      this.$store.commit('modal', false)
      this.$store.commit('panel', false)
      this.$store.commit('detail', false)
      this.$store.commit('api', false)
      this.$store.commit('tip', false)
      this.$store.commit('content', false)
      this.$store.commit('communication', {})
      this.$store.commit('menu', '')
      localStorage.clear()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./login.scss";
</style>
