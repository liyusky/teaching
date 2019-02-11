<template>
  <!-- s 教师列表 -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">序号</th>
        <th class="table-110">姓名</th>
        <th class="table-130">手机</th>
        <th class="table-70">性别</th>
        <th class="table-110">身份</th>
        <!-- <th class="table-150">学校</th> -->
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="table-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateTeacher(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110" :class="{'bg-red': !item.name}">{{item.name ? item.name : '未实名'}}</td>
          <td class="table-130" :class="{'bg-red': !item.phone}">{{item.phone ? item.phone : '未绑定'}}</td>
          <td class="table-70">{{item.sex ? '男' : '女'}}</td>
          <td class="table-110" :class="{'bg-red': !item.role && item.role != 0}">{{role[item.role]}}</td>
          <!-- <td class="table-150">{{getCollege(item.detail)}}</td> -->
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
  <!-- s 教师列表 -->
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
      table: [],
      role: Dictionary.role,
      rank: Dictionary.rank
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getTeacherList()
  },
  methods: {
    // getCollege (detail) {
    //   if ('college' in detail) {
    //     return `${detail.college.name}${detail.college.district && detail.college.district !== 'null' ? detail.college.district : ''}${Dictionary.rank[detail.college.level]}`
    //   } else {
    //     return '未设置'
    //   }
    // },
    getTeacherList (keywords) {
      let data = {}
      if (keywords) {
        data.keywords = keywords
      }
      Http.send({
        url: 'TeacherList',
        data: data
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateTeacher',
        data: {
          tid: item.user,
          enable: item.enable ? 0 : 1
        }
      }).before(() => {
        this.table[index].disabled = true
      }).success(data => {
        this.table[index].enable = !item.enable
      }).fail(data => {
      }).default(() => {
        this.table[index].disabled = false
        Display.api = false
      })
    },
    updateTeacher (item) {
      Communication.panel = item
      Display.panel = 'teacher-update-teacher'
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'TeacherList') {
        this.getTeacherList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
