<template>
  <!-- s 课程列表 -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">详情</th>
        <th class="table-70">修改</th>
        <th class="table-70">序号</th>
        <th class="table-150">名称</th>
        <th class="table-90">语言</th>
        <th class="table-130">创建人</th>
        <th class="table-90">适用年级</th>
        <th class="table-210">描述</th>
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
            <button class="content-show-detail" :disabled="!item.enable" @click="updateCourse(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-150">{{item.name}}</td>
          <td class="table-90">{{language[item.language]}}</td>
          <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-90">{{rank[item.grade]}}</td>
          <td class="table-210" :title="item.description">{{item.description}}</td>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.cid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s 课程列表 -->
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
      language: Dictionary.language,
      rank: Dictionary.rank,
      enableClass: true
      // start datas
      // end datas
    }
  },
  created () {
    this.getCourseList()
  },
  methods: {
    openDetail (item) {
      Display.detail = 'course'
      Communication.detail = item
    },
    getCourseList () {
      Http.send({
        url: 'CourseList'
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateCourse',
        data: {
          cid: item.cid,
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
    updateCourse (item) {
      Communication.panel = item
      Display.panel = 'course-update-course'
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'CourseList') {
        this.getCourseList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
