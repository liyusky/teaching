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
  static notNeedTokenApi = ['LoginByPassword', 'ForgetPassword', 'Register', 'SMSCaptcha']
  static baseUrl = 'http://192.168.1.5:8080/teaching'
  static grade = ['未知', '小一', '小二', '小三', '小四', '小五', '小六', '初一', '初二', '初三', '高一', '高二', '高三']
  static role = ['学生', '老师', '管理员', 'root']
  static status = {
    student: ['未决定', '学习中', '结业', '肄业']
  }
  static language = ['未知', '综合', 'PASCAL', 'C', 'C++']
  static rank = ['未定', '综合', '小学', '初中', '高中']
  static Game = ['酷町猫', '酷町打字']
  static page = {
    'student': `课程列表`,
    'student-lesson': '课程内容',
    'student-stage': '游戏章节内容',
    'student-homework': '作业详情',
    'student-example': '课时详情',
    'student-code': '代码详情',
    'student-record': '提交记录'
  }
}
