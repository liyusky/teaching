export default class Storage {
  static set addNav (page) {
    let nav = this.getStorage('nav')
    nav.push(page)
    this.save('nav', nav)
  }

  static set adjustNav (index) {
    let nav = this.getStorage('nav')
    nav = nav.slice(0, index)
    this.save('nav', nav)
  }

  static get nav () {
    let nav = this.getStorage('nav')
    return nav
  }

  static save (item, value) {
    window.main.$store.commit(item, value)
    try {
      localStorage.setItem(item, JSON.stringify(value))
    } catch (error) {}
  }

  static getStorage (item) {
    let result = null
    try {
      result = localStorage.getItem(item)
      if (result) {
        result = JSON.parse(localStorage.getItem(item))
      } else {
        result = []
      }
    } catch (error) {}
    return [...result]
  }

  static initNav () {
    let nav = this.nav
    window.main.$store.commit('nav', nav)
  }
}
