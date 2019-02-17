export default class Communication {
  static set cview (cview) {
    let communication = this.getStorage('communication')
    communication.cview = cview
    this.save('communication', communication)
  }

  static get cview () {
    let communication = this.getStorage('communication')
    return communication.cview
  }

  static set substance (substance) {
    let communication = this.getStorage('communication')
    communication.substance = substance
    this.save('communication', communication)
  }

  static get substance () {
    let communication = this.getStorage('communication')
    return communication.substance
  }

  static set detail (detail) {
    let communication = this.getStorage('communication')
    communication.detail = detail
    this.save('communication', communication)
  }

  static get detail () {
    let communication = this.getStorage('communication')
    return communication.detail
  }

  static set panel (panel) {
    let communication = this.getStorage('communication')
    communication.panel = panel
    this.save('communication', communication)
  }

  static get panel () {
    let communication = this.getStorage('communication')
    return communication.panel
  }

  static set modal (modal) {
    let communication = this.getStorage('communication')
    communication.modal = modal
    this.save('communication', communication)
  }

  static get modal () {
    let communication = this.getStorage('communication')
    return communication.modal
  }

  static save (item, value) {
    window.manager.$store.commit(item, value)
    try {
      localStorage.setItem(item, JSON.stringify(value))
    } catch (error) {}
  }

  static getStorage (item) {
    let result = null
    try {
      result = JSON.parse(localStorage.getItem(item))
    } catch (error) {}
    // if (this.isEmpty(result)) {
    //   this.save(item, result)
    // } else if (this.notEmpty(item)) {
    //   result = window.manager.$store.state[item]
    //   this.save(item, result)
    // }
    return {...result}
  }

  // static notEmpty (item) {
  //   let result = false
  //   let content = window.manager.$store.state[item]
  //   let keys = ['lesson', 'modal', 'stage', 'code', 'example', 'homework', 'record']
  //   keys.forEach(key => {
  //     if (key in content) result = true
  //   })
  //   return result
  // }

  // static isEmpty (data) {
  //   let result = false
  //   if (data !== null && data !== '' && data !== undefined) result = true
  //   return result
  // }
}
