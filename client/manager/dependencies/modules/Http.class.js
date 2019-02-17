import axios from 'axios'
import MangerUrl from './MangerUrl.class.js'
import TeacherUrl from './TeacherUrl.class'
import Account from './Account.class.js'
import Router from './Router.class.js'
import Dictionary from './Dictionary.class.js'
export default class Http {
  beforeCallback = null
  successCallback = null
  failCallback = null
  defaultCallback = null
  static send (args) {
    var Url = MangerUrl
    let instance = new Http()
    args.data = args.data ? args.data : {}
    var headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
    var datas = new URLSearchParams()
    if (!Dictionary.notNeedTokenApi.includes(args.url)) {
      headers['Authorization'] = `JWT ${Account.token}`
    }
    for (const key in args.data) {
      datas.append(key, args.data[key])
    }

    if (instance.beforeCallback) instance.beforeCallback()

    if (Account.role > 0 && Account.role < 99 && args.url in TeacherUrl) {
      Url = TeacherUrl
    }

    axios({
      url: Url[args.url],
      method: 'post',
      baseURL: window.baseUrl,
      withCredentials: true,
      headers: headers,
      data: datas
    }).then(response => {
      Account.token = response.data.token
      instance.dispense(response.data)
      if (instance.defaultCallback) instance.defaultCallback()
    }).catch(error => {
      console.log(error.response)
      if (error.response) {
        if (error.response.status === 401) {
          Router.push('login')
        }
        let data = error.response.data
        if ('token' in data) {
          Account.token = data.token
        }
        if ('description' in data) {
          alert(data.description)
        }
        if ('detail' in data) {
          alert(data.detail)
          if (data.detail === '您不具有教师权限！') {
            Router.push('login')
          }
        }
      }
      if (instance.defaultCallback) instance.defaultCallback()
    })
    return instance
  }
  dispense (response) {
    switch (response.code) {
      case 200:
        if (this.successCallback) this.successCallback(response.data)
        break
      default:
        window.modal.$store.commit('saveError', {
          modal: true,
          message: response.message
        })
        if (this.failCallback) this.failCallback(response)
    }
  }
  before (callback) {
    this.beforeCallback = callback
    return this
  }
  success (callback) {
    this.successCallback = callback
    return this
  }
  fail (callback) {
    this.failCallback = callback
    return this
  }
  default (callback) {
    this.defaultCallback = callback
    return this
  }
}
