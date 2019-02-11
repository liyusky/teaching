export default class Display {

  static set detail (detail) {
    this.save('detail', detail)
  }

  static get detail () {
    return this.getStorage('detail')
  }

  static set panel (panel) {
    this.save('panel', panel)
  }

  static get panel () {
    return this.getStorage('panel')
  }

  static get modal () {
    return this.getStorage('modal')
  }

  static set modal (modal) {
    this.save('modal', modal)
  }

  static set api (api) {
    this.save('api', api)
  }

  static get api () {
    return this.getStorage('api')
  }

  static set content (content) {
    this.save('content', content)
  }

  static get content () {
    return this.getStorage('content')
  }

  static set tip (tip) {
    this.save('tip', tip)
  }

  static get tip () {
    return this.getStorage('tip')
  }

  static save (item, value) {
    window.main.$store.commit(item, value)
  }

  static getStorage (item) {
    return window.main.$store.state[item]
  }
}
