export default class Check {
  static imageCode (code) {
    code = code ? code.replace(/\s+/g, '') : code
    if (!code) {
      this.show('请输入图形验证码')
      return false
    }
    if (code.length < 4) {
      this.show('图形验证码长度不足4位')
      return false
    } else if (code.length > 4) {
      this.show('图形验证码长度多于4位')
      return false
    }
    let reg = new RegExp('^[a-zA-Z0-9]{4}$', 'i')
    if (!reg.test(code)) {
      this.show('图形验证码格式错误')
      return false
    }
    return true
  }

  static smsCode (code) {
    code = code ? code.replace(/\s+/g, '') : code
    if (!code) {
      this.show('请输入短信验证码')
      return false
    }
    if (code.length < 6) {
      this.show('短信验证码长度不足6位')
      return false
    } else if (code.length > 6) {
      this.show('短信验证码长度多于6位')
      return false
    }
    let reg = new RegExp('^[0-9]{6}$', 'i')
    if (!reg.test(code)) {
      this.show('短信验证码格式错误')
      return false
    }
    return true
  }

  static sex (sex) {
    sex += ''
    sex = sex ? sex.replace(/\s+/g, '') : sex
    if (!sex) {
      this.show('请选择性别')
      return false
    }
    if (!(sex * 1 in [0, 1])) {
      this.show('性别格式错误')
      return false
    }
    return true
  }

  static role (role) {
    role += ''
    role = role ? role.replace(/\s+/g, '') : role
    if (!role) {
      this.show('请选择角色')
      return false
    }
    if (!(role * 1 in ranger(4))) {
      this.show('角色格式错误')
      return false
    }
    return true
  }

  static grade (grade) {
    grade += ''
    grade = grade ? grade.replace(/\s+/g, '') : grade
    if (!grade) {
      this.show('请选择年级')
      return false
    }
    if (!(grade * 1 in ranger(13))) {
      this.show('角色格式错误')
      return false
    }
    return true
  }

  static scene (scene) {
    scene += ''
    scene = scene ? scene.replace(/\s+/g, '') : scene
    if (!scene) {
      this.show('请输入场景编号')
      return false
    }
    if (!(scene * 1 in [0, 1, 2])) {
      this.show('场景编号应该为[0, 1, 2]中的值')
      return false
    }
    return true
  }

  static name (name) {
    name = name ? name.replace(/\s+/g, '') : name
    if (!name) {
      this.show('请输入姓名')
      return false
    }
    if (name.length < 2) {
      this.show('姓名长度不足2位')
      return false
    }

    let pat = new RegExp(/^[\u4E00-\u9FA5]{2,}(?:·[\u4E00-\u9FA5]{2,5})*/)
    if (!pat.test(name)) {
      this.show('姓名格式错误')
      return false
    }
    return true
  }

  static account (account) {
    account = account ? account.replace(/\s+/g, '') : account
    if (!account) {
      this.show('请输入账户')
      return false
    }

    if (account.length < 6) {
      this.show('账户长度不足6位')
      return false
    }

    let pat = new RegExp(/[A-Za-z0-9_\-]{6,30}/)
    if (!pat.test(account)) {
      this.show('账户格式错误')
      return false
    }
    return true
  }

  static age (age) {
    age = age ? age.replace(/\s+/g, '') : age
    age = parseInt(age)
    if (isNaN(age * 1)) {
      this.show('请输入数字')
      return false
    }

    if (age % 1) {
      this.show('请输入正整数')
      return false
    }

    if (age <= 0 || age > 100) {
      this.show('请输入1到100范围内的正整数')
      return false
    }
    return true
  }


  static appellation (appellation) {
    appellation = appellation ? appellation.replace(/\s+/g, '') : appellation
    if (!appellation) {
      this.show('请输入名称')
      return false
    }
    if (appellation.length < 2) {
      this.show('名称长度不足2位')
      return false
    }

    let pat = new RegExp(/[^;]+/)
    if (!pat.test(appellation)) {
      this.show('名称不可以含有分号')
      return false
    }

    pat = new RegExp(/[\S]{2,100}/)
    if (!pat.test(appellation)) {
      this.show('名称格式错误')
      return false
    }
    return true
  }

  static dateRange (date) {
    date = date ? date.replace(/\s+/g, '') : date
    if (!date) {
      this.show('请选择时间')
      return false
    }
    if (!date.includes('to')) {
      this.show('请选定时间范围')
      return false
    }
    return true
  }

  static password (password) {
    password = password ? password.replace(/\s+/g, '') : password
    if (!password) {
      this.show('密码不能为空')
      return false
    }
    if (password.length < 6 || password.length > 20) {
      this.show('密码长度为6-20个字符')
      return false
    }
    let pat = new RegExp(/^\S{6,20}$/)
    if (!pat.test(password)) {
      this.show('密码格式错误，可选择字母，数字，非空字符')
      return false
    }
    return true
  }

  static username (username) {
    username = username ? username.replace(/\s+/g, '') : username
    if (!username) {
      this.show('用户名不能为空')
      return false
    }
    if (username.length < 6 || username.length > 30) {
      this.show('用户名长度为6-30个字符')
      return false
    }
    let pat = new RegExp(/^[a-zA-Z0-9]{6,30}$/)
    if (!pat.test(username)) {
      this.show('用户名格式错误，可选择数字或者字母')
      return false
    }
    return true
  }

  static phone (phone) {
    phone = phone ? phone.replace(/\s+/g, '') : phone
    if (!phone) {
      this.show('请输入手机号')
      return false
    }
    if (phone.length < 11) {
      this.show('手机号长度不足11位')
      return false
    } else {
      let reg = new RegExp('^(?:13|14|15|17|18)[0-9]{9}$', 'i')
      if (!reg.test(phone)) {
        this.show('手机号格式错误')
        return false
      }
      return true
    }
  }

  static show (message) {
    alert(message)
    // window.modal.$store.commit('saveError', {
    //   modal: true,
    //   message: message
    // })
  }
}

function ranger (start = 0, end) {
  let arr = []
  while (start < end) {
    arr.push(start)
    start++
  }
  return arr
}
