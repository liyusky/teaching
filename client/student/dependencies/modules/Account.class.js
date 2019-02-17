import Router from './Router.class.js'

export default class Account {
  static set info (account) {
    let customer = {
      age: account.age,
      uid: account.user,
      upid: account.upid,
      phone: account.phone,
      name: account.name,
      sex: account.sex,
      role: account.role,
      // school: account.school,
      // college: account.detail.college,
      grade: account.grade,
      creator: account.creator,
      description: account.description
    }
    customer.token = Account.token
    this.save('account', customer)
  }

  static get token () {
    let account = this.getStorage('account')
    return account.token
  }

  static set token (token) {
    let account = this.getStorage('account')
    account.token = token
    this.save('account', account)
  }

  static get uid () {
    let account = this.getStorage('account')
    return account.uid
  }

  static get phone () {
    let account = this.getStorage('account')
    return account.phone
  }

  static get name () {
    let account = this.getStorage('account')
    return account.name
  }

  static get sex () {
    let account = this.getStorage('account')
    return account.sex
  }

  static get role () {
    let account = this.getStorage('account')
    return account.role
  }

  // static get school () {
  //   let account = this.getStorage('account')
  //   return account.school
  // }

  static get grade () {
    let account = this.getStorage('account')
    return account.grade
  }

  static get creator () {
    let account = this.getStorage('account')
    return account.creator
  }

  static set description (description) {
    let account = this.getStorage('account')
    account.description = description
    this.save('account', account)
  }

  static get description () {
    let account = this.getStorage('account')
    return account.description
  }

  static get upid () {
    let account = this.getStorage('account')
    return account.upid
  }

  static get age () {
    let account = this.getStorage('account')
    return account.age
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

  static logout () {
    if (!Account.uid) {
      Router.push('login')
    }
  }
}
