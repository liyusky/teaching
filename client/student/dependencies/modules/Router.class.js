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
}
