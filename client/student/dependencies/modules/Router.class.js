import Dictionary from './Dictionary.class.js'
import Storage from './Storage.class.js'
export default class Router {
  static push (params) {
    if (typeof params === 'string') {
      params = {
        name: params
      }
    }
    if (params.name in Dictionary.page) {
      Storage.addNav = {
        name: Dictionary.page[params.name],
        page: params.name
      }
    }
    window.main.$router.push(params)
  }

  static set target (page) {
    let params = {}
    if (typeof page === 'string') {
      params.name = page
    } else {
      params = page
    }
    window.main.$router.push(params)
  }

  static refreshAuth () {
    this.saveOldStorage()
    window.main.$router.push({
      path: '/',
      query: {
        next: window.main.$route.name,
        type: 1
      }
    })
  }

  static saveOldStorage () {
    let accountBack = window.localStorage.getItem('account')
    window.localStorage.setItem('accountBack', accountBack)
    let navBack = window.localStorage.getItem('nav')
    window.localStorage.setItem('navBack', navBack)
    let communicationBack = window.localStorage.getItem('communication')
    window.localStorage.setItem('communicationBack', communicationBack)
    window.localStorage.removeItem('account')
    window.localStorage.removeItem('nav')
    window.localStorage.removeItem('communication')
  }

  static transformNewStorage () {
    let account = window.localStorage.getItem('accountBack')
    window.localStorage.setItem('account', account)
    let nav = window.localStorage.getItem('navBack')
    window.localStorage.setItem('nav', nav)
    let communication = window.localStorage.getItem('communicationBack')
    window.localStorage.setItem('communication', communication)
    window.localStorage.removeItem('accountBack')
    window.localStorage.removeItem('navBack')
    window.localStorage.removeItem('communicationBack')
  }
}
