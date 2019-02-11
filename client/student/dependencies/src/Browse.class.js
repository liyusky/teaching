export default class Browse {
  static set info (browse) {
    browse = {
      category: browse.category
    }
    this.save(browse)
  }

  static set category (category) {
    let browse = {...window.app.$store.state.browse}
    browse.category = category
    this.save(browse)
  }

  static get category () {
    let browse = this.getStorage()
    return browse.category
  }

  static save (browse) {
    window.app.$store.commit('saveBrowse', browse)
    try {
      localStorage.setItem('student', JSON.stringify(browse))
    } catch (error) {}
  }

  static getStorage () {
    let storage = null
    try {
      storage = JSON.parse(localStorage.getItem('browse'))
    } catch (error) {}
    if (window.app.$store.state.browse !== null) {
      storage = {...window.app.$store.state.browse}
    } else if (storage !== null) {
      this.save(storage)
    }
    return storage
  }
}
