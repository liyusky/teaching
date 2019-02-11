<template>
  <!-- s 课程列表 -->
  <section class="class">
    <table class="class-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">修改</th>
        <th class="table-70">序号</th>
        <th class="table-110">名称</th>
        <th class="table-130">班主任</th>
        <th class="table-70">状态</th>
        <th class="table-70">课程</th>
        <th class="table-70">学生</th>
        <th class="table-100">开始</th>
        <th class="table-100">结束</th>
        <th class="table-130">创建人</th>
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="class-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="showDetail(item)">详情</button>
          </td>
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateClass(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110" :title="item.name">{{item.name}}</td>
          <td class="table-130">{{item.manager.name}}（{{item.manager.phone}}）</td>
          <td class="table-70">{{setStatus(item)}}</td>
          <td class="table-70">{{item.courses.length}}</td>
          <td class="table-70">{{item.students.length}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD', item.launch)}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD', item.deadline)}}</td>
          <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.oid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s 课程列表 -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'ClassTableComponent',
  data () {
    return {
      table: [],
      TimeModule: Time
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getClassList()
  },
  methods: {
    setStatus (item) {
      let status = '进行中'
      let now = (new Date()).getTime()
      if (now < (new Date(item.launch)).getTime()) status = '未开始'
      if (now > (new Date(item.deadline)).getTime()) status = '已结束'
      return status
    },
    showDetail (item) {
      Display.detail = 'class'
      Communication.detail = item
    },
    getClassList () {
      Http.send({
        url: 'ClassList'
      }).success(data => {
        this.table = data
      }).fail(data => {
        console.log(data)
      }).default(() => {
        Display.api = false
      })
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateClass',
        data: {
          oid: item.oid,
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
    updateClass (item) {
      Communication.panel = item
      Display.panel = 'class-update-class'
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'ClassList') {
        this.getClassList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./class.scss";
</style>
