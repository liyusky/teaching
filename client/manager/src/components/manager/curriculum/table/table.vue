<template>
  <!-- s  -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">序号</th>
        <th class="table-150">课时</th>
        <th class="table-100">开始</th>
        <th class="table-100">结束</th>
        <!-- <th class="table-170">地点</th> -->
        <th class="table-130">创建人</th>
        <th class="table-70">启用</th>
        <th class="table-70">作业</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="table-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateCurriculum(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-150">{{item.lessonDetail}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD HH:mm', item.launch)}}</td>
          <td class="table-100">{{TimeModule.format('YYYY-MM-DD HH:mm', item.deadline)}}</td>
          <!-- <td class="table-170">{{item.college.name}}{{item.college.district || ''}}{{item.classroom}}</td> -->
          <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">
            <button class="content-show-detail" :class="{'fail-btn': item.task}" :disabled="!item.enable || item.task" @click="addHomework(item)">{{item.task ? '已有' : '生成'}}</button>
          </td>
          <td class="table-70">{{item.curid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'CurriculumTableComponent',
  props: ['oid', 'cid', 'course', 'organization'],
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
    this.getCurriculumList()
  },
  methods: {
    getCurriculumList () {
      if (this.oid > 0 && this.cid > 0) {
        Http.send({
          url: 'CurriculumList',
          data: {
            oid: this.oid,
            cid: this.cid
          }
        }).success(data => {
          this.table = data
        }).fail(data => {
        }).default(() => {
          Display.api = false
        })
      }
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateCurriculum',
        data: {
          curid: item.curid,
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
    updateCurriculum (item) {
      if (this.course === '选择课程') {
        alert('未选择课程')
        return
      }
      if (this.organization === '选择班级') {
        alert('未选择班级')
        return
      }
      item.oid = this.oid
      item.cid = this.cid
      item.course = this.course
      item.organization = this.organization
      Communication.panel = item
      Display.panel = 'curriculum-update-curriculum'
    },
    addHomework (item) {
      if (this.course === '选择课程') {
        alert('未选择课程')
        return
      }
      if (this.organization === '选择班级') {
        alert('未选择班级')
        return
      }
      item.oid = this.oid
      item.cid = this.cid
      item.lid = this.lid
      Communication.panel = item
      Display.panel = 'homework-add-homework'
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'CurriculumList') {
        this.getCurriculumList()
        Display.api = false
      }
    },
    oid () {
      this.getCurriculumList()
    },
    cid () {
      this.getCurriculumList()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
