<template>
  <!-- s  -->
  <section class="inputs" :class="inputs.type">
    <div class="left">
      <i class="iconfont left-icon" :class="'icon-' + inputs.leftIcon" v-if="inputs.leftIcon"></i>
      <div class="left-text" v-if="inputs.leftText">{{inputs.leftText}}</div>
    </div>
    <div class="right">
      <input class="right-input" v-if="inputs.style" :type="inputs.style ? inputs.style : 'text'" :maxlength="inputs.maxLength" :disabled="inputs.dsiabled" v-model="inputText" :placeholder="inputs.placeholder">
      <i class="iconfont right-icon" :class="'icon-' + inputs.rightIcon" v-if="inputs.rightIcon" @click="clearInput"></i>
      <p class="right-text" v-if="inputs.rightText">{{inputs.rightText}}</p>
      <!-- <div class="right-switch" :class="{'switch-active': switchShow}" v-if="inputs.type === 'switch'" @click="switchToggle">
        <div class="switch-btn"></div>
      </div> -->
      <div class="right-image" v-if="inputs.imageCode" @click="getImageCode">
        <img :src="imageCode">
      </div>
      <button class="right-sms" :disabled="sendSMSDisabled" v-if="inputs.smsCode" @click="sendSMSCaptcha">{{sendSMSBtnText}}</button>
      <div class="right-sex" v-if="inputs.sex">
        <label class="sex-item">
          <input type="radio" name="sex" :value="0" v-model="sex">
          <span>男</span>
        </label>
        <label class="sex-item">
          <input type="radio" name="sex" :value="1" v-model="sex">
          <span>女</span>
        </label>
      </div>
    </div>
  </section>
  <!-- e  input组件-->
</template>

<script>
// include dependence
import Check from '../../modules/Check.class.js'
import Dictionary from '../../modules/Dictionary.class.js'
import Http from '../../modules/Http.class.js'

export default {
  name: 'InputComponent',
  props: ['inputs', 'sms', 'scene'],
  data () {
    return {
      imageCode: `${Dictionary.baseUrl}/common/image-code?time=${new Date()}`,
      sex: '',
      inputText: '',
      switchShow: true,
      sendSMSDisabled: false,
      sendSMSBtnText: '获取短信验证码'
    }
  },
  created () {
    this.inputText = this.inputs.receiveInput
    this.$on('getImageCode', this.getImageCode)
  },
  methods: {
    openModal () {
      if (this.inputs.type !== 'center') return
      if (this.inputs.type !== 'default') return
      if (this.inputs.type !== 'swicth') return
      this.$emit('OPEN_MODAL_EVENT')
    },
    switchToggle () {
      if (this.inputs.type === 'switch') {
        this.switchShow = !this.switchShow
        this.$emit('SWITCH_TOGGLE_EVENT', this.switchShow)
      }
    },
    clearInput () {
      if (this.inputs.type !== 'default') return
      this.inputText = ''
      this.$emit('CLEAR_INPUT_EVENT')
    },
    getImageCode () {
      this.imageCode = `${Dictionary.baseUrl}/common/image-code?time=${new Date()}`
    },
    sendSMSCaptcha () {
      if (!Check.phone(this.sms.account)) return
      if (!Check.imageCode(this.sms.imageCode)) return
      if (!Check.scene(this.scene)) return
      // this.waitOneMinute()
      Http.send({
        url: 'SMSCaptcha',
        data: {
          account: this.sms.account,
          imageCode: this.sms.imageCode,
          scene: this.scene
        }
      }).success(data => {
      }).fail(data => {
        console.log(data)
      })
    },
    waitOneMinute () {
      this.sendSMSDisabled = true
      this.sendSMSBtnText = '60秒后重发'
      let time = 60
      let animation = setInterval(() => {
        time--
        if (time > 0) {
          this.sendSMSBtnText = `${time}秒后重发`
        } else {
          this.sendSMSBtnText = '获取短信验证码'
          clearInterval(animation)
          this.sendSMSDisabled = false
        }
      }, 1000)
    }
  },
  watch: {
    inputText (newValue, oldValue) {
      this.$emit('GET_INPUT_TEXT_EVENT', newValue)
    },
    sex (newValue, oldValue) {
      this.$emit('GET_SEX_EVENT', newValue)
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./inputs.scss";
</style>
