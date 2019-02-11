<template>
  <!-- s 作业列表 -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">详情</th>
        <th class="table-70">修改</th>
        <th class="table-70">序号</th>
        <th class="table-110">名称</th>
        <th class="table-110">班级</th>
        <th class="table-110">课时</th>
        <th class="table-130">备注</th>
        <th class="table-100">开始</th>
        <th class="table-100">结束</th>
        <th class="table-130">创建人</th>
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="table-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="openDetail(item)">详情</button>
          </td>
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateHomework(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110" :title="item.name">{{item.name}}</td>
          <td class="table-110" :title="item.curriculumDetail.organization.name">{{item.curriculumDetail.organization.name}}</td>
          <td class="table-110" :title="item.curriculumDetail.lesson">{{item.curriculumDetail.lesson}}</td>
          <td class="table-130" :title="item.description">{{item.description}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD HH:mm', item.launch)}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD HH:mm', item.deadline)}}</td>
          <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.hid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s 作业列表 -->
</template>

<script>
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'TableComponent',
  props: ['oid', 'cid', 'lid', 'gcid'],
  data () {
    return {
      TimeModule: Time,
      table: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getHomeworkList()
  },
  methods: {
    getHomeworkList () {
      let data = {}
      if (this.oid > 0) data.oid = this.oid
      if (this.cid > 0) data.cid = this.cid
      if (this.lid > 0) data.lid = this.lid
      if (this.gcid > 0) data.gcid = this.gcid
      Http.send({
        url: 'HomeworkList',
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
        url: 'UpdateHomework',
        data: {
          hid: item.hid,
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
    updateHomework (item) {
      Communication.panel = item
      Display.panel = 'homework-update-homework'
    },
    openDetail (item) {
      Display.detail = 'homework'
      Communication.detail = item
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'HomeworkList') {
        this.getHomeworkList()
        Display.api = false
      }
    },
    oid () {
      this.getHomeworkList()
    },
    cid () {
      this.getHomeworkList()
    },
    lid () {
      this.getHomeworkList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
