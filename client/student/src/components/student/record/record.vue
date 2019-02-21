<template>
  <!-- s  -->
  <section class="record">
    <div class="record-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-100">序号</th>
          <th class="table-100">结果</th>
          <th class="table-100">成绩</th>
          <th class="table-130">提交时间</th>
          <th class="table-100">代码</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index">
            <td class="table-100">{{index + 1}}</td>
            <td class="table-100">{{item.success ? '成功' : '失败'}}</td>
            <td class="table-100">{{item.score}}</td>
            <td class="table-130">{{TimeModule.format('YYYY-MM-DD HH-mm-ss', item.time)}}</td>
            <td class="table-100">
              <button class="content-show-detail" @click="showCode(item, index)">查看</button>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../../../dependencies/modules/Account.class.js'
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'
import Router from '../../../../dependencies/modules/Router.class.js'
import Time from '../../../../dependencies/modules/Time.class.js'

export default {
  name: 'RecordComponent',
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
    Account.logout()
    this.getGameStageRecode()
  },
  methods: {
    showCode (item, index) {
      let content = {...item}
      content.chapter = Communication.record.chapter
      content.stage = Communication.record.name
      content.submit = index
      Communication.code = content
      switch (this.$route.name) {
        case 'student-example-record':
          Router.push(`student-example-code`)
          break
        case 'student-homework-record':
          Router.push(`student-homework-code`)
          break
      }
    },
    getGameStageRecode () {
      Http.send({
        url: 'GameStageRecord',
        data: {
          gsid: Communication.record.gsid,
          student: Account.uid
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
@import "./record.scss";
</style>
