<template>
  <!-- s  -->
  <section class="plan">
    <table class="plan-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">序号</th>
        <th class="table-110">名称</th>
        <th class="table-130">老师</th>
        <th class="table-70">状态</th>
        <th class="table-100">开始</th>
        <th class="table-100">结束</th>
        <th class="table-130">创建人</th>
        <th class="table-70">详情</th>
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="plan-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updatePlan(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110">{{item.courseDetail.name}}</td>
          <td class="table-130">{{item.teacherDetail.name}}（{{item.teacherDetail.phone}}）</td>
          <td class="table-70">{{setStatus(item)}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD', item.launch)}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD', item.deadline)}}</td>
          <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="openLesson(item)">查看</button>
          </td>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.pid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'PlanTableComponent',
  props: ['table'],
  data () {
    return {
      TimeModule: Time
      // start datas
      // end datas
    }
  },
  methods: {
    setStatus (item) {
      let status = '进行中'
      let now = (new Date()).getTime()
      if (now < (new Date(item.launch)).getTime()) status = '未开始'
      if (now > (new Date(item.deadline)).getTime()) status = '已结束'
      return status
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdatePlan',
        data: {
          pid: item.pid,
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
    updatePlan (item) {
      item.organization = {...Communication.detail}
      Communication.panel = item
      Display.panel = 'plan-update-plan'
    },
    openLesson (item) {
      Communication.substance = item
      Display.substance = 'lesson'
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./plan.scss";
</style>
