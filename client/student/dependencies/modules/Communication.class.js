export default class Communication {

  static set lesson (lesson) {
    let communication = this.getStorage('communication')
    communication.lesson = lesson
    this.save('communication', communication)
  }

  static get lesson () {
    let communication = this.getStorage('communication')
    return communication.lesson
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

  static set stage (stage) {
    let communication = this.getStorage('communication')
    communication.stage = stage
    this.save('communication', communication)
  }

  static get stage () {
    let communication = this.getStorage('communication')
    return communication.stage
  }

  static set code (code) {
    let communication = this.getStorage('communication')
    communication.code = code
    this.save('communication', communication)
  }

  static get code () {
    let communication = this.getStorage('communication')
    return communication.code
  }

  static set example (example) {
    let communication = this.getStorage('communication')
    communication.example = example
    this.save('communication', communication)
  }

  static get example () {
    let communication = this.getStorage('communication')
    return communication.example
  }

  static set homework (homework) {
    let communication = this.getStorage('communication')
    communication.homework = homework
    this.save('communication', communication)
  }

  static get homework () {
    let communication = this.getStorage('communication')
    return communication.homework
  }

  static set record (record) {
    let communication = this.getStorage('communication')
    communication.record = record
    this.save('communication', communication)
  }

  static get record () {
    let communication = this.getStorage('communication')
    return communication.record
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
    return {...result}
  }
}
