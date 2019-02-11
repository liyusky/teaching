import axios from 'axios'
import Url from './Url.class.js'
import Account from './Account.class.js'
import Dictionary from './Dictionary.class.js'
import Router from './Router.class.js'
export default class Http {
  beforeCallback = null
  successCallback = null
  failCallback = null
  defaultCallback = null
  static send (args) {
    let instance = new Http()
    args.data = args.data ? args.data : {}

    var datas = new URLSearchParams()
    var headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
    if (!Dictionary.notNeedTokenApi.includes(args.url)) {
      headers['Authorization'] = `JWT ${Account.token}`
    }
    for (const key in args.data) {
      datas.append(key, args.data[key])
    }

    if (instance.beforeCallback) instance.beforeCallback()

    axios({
      url: Url[args.url],
      method: 'post',
      baseURL: window.baseUrl,
      withCredentials: true,
      headers: headers,
      data: datas
    }).then(response => {
      if ('token' in response.data) Account.token = response.data.token
      instance.dispense(response.data, args.url)
      if (instance.defaultCallback) instance.defaultCallback()
    }).catch(error => {
      if (error.response) {
        if (error.response.status === 401) {
          Router.push('login')
        }
        let data = error.response.data
        if ('description' in data) alert(data.description)
      }
      if (instance.defaultCallback) instance.defaultCallback()
    })
    return instance
  }
  dispense (response, url) {
    if (url === 'GetToken') {
      if (this.successCallback) this.successCallback(response.token)
    } else {
      switch (response.code) {
        case 200:
          if (this.successCallback) this.successCallback(response.data)
          break
        default:
          if (this.failCallback) this.failCallback(response)
      }
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
