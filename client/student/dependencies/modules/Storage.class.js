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
      result = JSON.parse(localStorage.getItem(item))
    } catch (error) {}
    console.log(result)
    if (this.notEmpty(item)) {
      result = window.main.$store.state[item]
    } else if (this.isEmpty(result)) {
      this.save(item, result)
    } else {
      result = []
      this.save(item, result)
    }
    return [...result]
  }



  static notEmpty (item) {
    let result = false
    let content = window.main.$store.state[item]
    if (content.length > 0) result = true
    return result
  }

  static isEmpty (data) {
    let result = false
    if (data !== null && data !== '' && data !== undefined && data === []) result = true
    return result
  }
}
