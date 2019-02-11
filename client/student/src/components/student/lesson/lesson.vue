<template>
  <!-- s  -->
  <section class="lesson">
    <div class="lesson-nav">
    </div>
    <section class="lesson-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-70">序号</th>
          <th class="table-110">名称</th>
          <th class="table-130">教师</th>
          <th class="table-210">描述</th>
          <th class="table-70">教学案例</th>
          <th class="table-70">作业</th>
          <th class="table-70">编号</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
            <td class="table-70">{{index + 1}}</td>
            <td class="table-110">{{item.name}}</td>
            <td class="table-130">{{teacher}}</td>
            <td class="table-210" :title="item.description">{{item.description}}</td>
            <td class="table-70">
              <button class="content-show-detail" @click="showExample(item)">查看</button>
            </td>
            <td class="table-70">
              <button class="content-show-detail" @click="showHomework(item)">查看</button>
            </td>
            <td class="table-70">{{item.lid}}</td>
          </tr>
        </table>
      </div>
    </section>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'
import Router from '../../../../dependencies/modules/Router.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'

export default {
  name: 'LessonComponent',
  data () {
    return {
      table: [],
      teacher: Communication.lesson.teacher
      // start datas
      // end datas
    }
  },
  created () {
    Account.logout()
    this.getLessonList()
  },
  methods: {
    showHomework (item) {
      Communication.homework = {
        ...item,
        oid: Communication.lesson.oid
      }
      Router.push('student-homework')
    },
    showExample (item) {
      Communication.example = item
      Router.push('student-example')
    },
    getLessonList () {
      Http.send({
        url: 'LessonList',
        data: {
          oid: Communication.lesson.oid,
          cid: Communication.lesson.cid
        }
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./lesson.scss";
</style>
