<template>
  <!-- s 学员列表 -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">序号</th>
        <th class="table-110">姓名</th>
        <th class="table-130">手机</th>
        <!-- <th class="table-150">学校</th> -->
        <th class="table-100">年级</th>
        <th class="table-100">性别</th>
        <!-- <th class="table-100">报名</th> -->
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="table-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateStudent(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110">{{item.name || '未实名'}}</td>
          <td class="table-130">{{item.phone}}</td>
          <!-- <td class="table-150">{{getCollege(item.detail)}}</td> -->
          <td class="table-100">{{grade[item.grade]}}</td>
          <td class="table-100">{{item.sex ? '男' : '女'}}</td>
          <!-- <td class="table-100">{{item.enroll ? '已报名' : '未报名'}}</td> -->
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.user}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s 学员列表 -->
</template>

<script>
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'TableComponent',
  data () {
    return {
      grade: Dictionary.grade,
      rank: Dictionary.rank,
      table: []
      // start datas
      // end datas
    }
  },
  created () {
    this.getStudentList()
  },
  methods: {
    // getCollege (detail) {
    //   if ('college' in detail) {
    //     return `${detail.college.name}${detail.college.district && detail.college.district !== 'null' ? detail.college.district : ''}${Dictionary.rank[detail.college.level]}`
    //   } else {
    //     return '未设置'
    //   }
    // },
    getStudentList (keywords) {
      let data = {}
      if (keywords) data.keywords = keywords
      Http.send({
        url: 'StudentList',
        data: data
      }).success(data => {
        this.table = data
        if (data.length === 0) {
          alert('暂无数据')
        }
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateStudent',
        data: {
          sid: item.user,
          enable: item.enable ? 0 : 1
        }
      }).before(() => {
        this.table[index].disabled = true
      }).success(data => {
        this.table[index].enable = !item.enable
        console.log(data)
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.table[index].disabled = false
        Display.api = false
      })
    },
    updateStudent (item) {
      Communication.panel = item
      Display.panel = 'student-update-student'
    },
    bindProfile () {
      Http.send({
        url: 'UserBindProfile'
      }).success(data => {
        this.getStudentList()
        let message = `共${data.count}位用户，${data.formerly}位已有详细简介，当前${data.add}位添加成功，${data.surplus}位添加失败，失败详情：${JSON.stringify(data.reason)}`
        alert(message)
      }).fail(data => {
        console.log(data)
      }).default(() => {
        this.$emit('User_Bind_Profile_OPEN_EVENT')
      })
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'StudentList') {
        this.getStudentList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
