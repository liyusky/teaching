export default class Dictionary {
  static role = {
    0: 'student',
    1: 'teacher',
    2: 'teacher'
  }
  static homework = {
    1: 'code',
    2: 'game'
  }
  static profession = {
    0: '学生',
    1: '教师',
    2: '教师'
  }
  static notNeedTokenApi = ['LoginByPassword', 'LoginBySMS', 'ForgetPassword', 'Register', 'SMSCaptcha']
  static grade = ['未知', '小一', '小二', '小三', '小四', '小五', '小六', '初一', '初二', '初三', '高一', '高二', '高三']
  static role = ['学生', '教学老师', '教务老师', '教务主任', '教学主任', '管理员', 'root']
  static role = {
    0: '学生',
    1: '教学老师',
    2: '教务老师',
    3: '教务主任',
    4: '教学主任',
    99: '管理员',
    100: 'root'
  }

  static status = {
    student: ['未决定', '学习中', '结业', '肄业']
  }
  static language = ['未知', '综合', 'PASCAL', 'C', 'C++']
  static rank = ['未定', '综合', '小学', '初中', '高中']
  static Game = ['酷町猫', '酷町打字']
}
