export default class Router {
  static push (params) {
    if (typeof params === 'string') {
      params = {
        name: params
      }
    }
    window.manager.$router.push(params)
  }

  static get menu () {
    let menu = this.getStorage('menu')
    return menu
  }

  static set menu (menu) {
    this.save('menu', menu)
  }


  static save (item, value) {
    window.manager.$store.commit(item, value)
    try {
      localStorage.setItem(item, value)
    } catch (error) {}
  }

  static getStorage (item) {
    let result = null
    try {
      result = localStorage.getItem(item)
    } catch (error) {}
    // if (this.notEmpty(item)) {
    //   result = window.manager.$store.state[item]
    // } else if (this.isEmpty(result)) {
    //   this.save(item, result)
    // }
    return result
  }

  static notEmpty (item) {
    let result = false
    let content = window.manager.$store.state[item]
    if (content) result = true
    return result
  }

  static isEmpty (data) {
    let result = false
    if (data !== null && data !== '' && data !== undefined) result = true
    return result
  }
}
