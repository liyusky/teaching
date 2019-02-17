import Router from './Router.class.js'
export default class Account {
  static set info (account) {
    let customer = {
      upid: account.upid,
      uid: account.user,
      phone: account.phone,
      name: account.name,
      sex: account.sex,
      age: account.age,
      role: account.role,
      // school: account.school,
      // college: account.detail.college ? account.detail.college : {
      //   name: '',
      //   district: '',
      //   level: 0,
      // },
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

  static get grade () {
    let account = this.getStorage('account')
    return account.grade
  }

  static get creator () {
    let account = this.getStorage('account')
    return account.creator
  }

  static get age () {
    let account = this.getStorage('account')
    return account.age
  }

  static get upid () {
    let account = this.getStorage('account')
    return account.upid
  }

  // static get college () {
  //   let account = this.getStorage('account')
  //   return account.college
  // }

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
    return {...result}
  }

  // static notEmpty (item) {
  //   let result = false
  //   let content = window.manager.$store.state[item]

  //   // let keys = ['uid', 'upid', 'phone', 'name', 'sex', 'role', 'school', 'grade', 'creator', 'description']
  //   let keys = ['uid', 'upid', 'phone', 'name', 'sex', 'role', 'grade', 'creator', 'description']
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

  static logout () {
    if (!Account.uid) {
      Router.push('login')
    }
  }
}
