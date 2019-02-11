<template>
  <!-- s  -->
  <section class="stage">
    <div class="stage-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-70">序号</th>
          <th class="table-130">名称</th>
          <th class="table-130">进度</th>
          <th class="table-70">最高分</th>
          <th class="table-70">游戏</th>
          <th class="table-70">提交记录</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index">
            <td class="table-70">{{index + 1}}</td>
            <td class="table-130">{{item.name}}</td>
            <td class="table-130">
              <ScheduleComponent :schedule="item.score"></ScheduleComponent>
            </td>
            <td class="table-70">{{item.score}}</td>
            <td class="table-70">
              <button class="content-show-detail" @click="taget(item.url)">跳转</button>
            </td>
            <td class="table-70">
              <button class="content-show-detail" @click="showRecode(item)">查看</button>
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
import ScheduleComponent from '../../../../dependencies/components/schedule/schedule.vue'
export default {
  name: 'StageComponent',
  data () {
    return {
      table: [],
      stage: [],
      score: [],
      stageMark: false,
      scoreMark: false
      // start datas
      // end datas
    }
  },
  components: {
    ScheduleComponent
    // include chunk
  },
  created () {
    Account.logout()
    this.getTable()
  },
  methods: {
    showRecode (item) {
      Communication.record = item
      Router.push('student-record')
    },
    getTable () {
      this.stageMark = false
      this.scoreMark = false
      this.getGameStageList()
      this.getGameStageScore()
    },
    getGameStageList () {
      Http.send({
        url: 'GameStageList',
        data: {
          gcid: Communication.stage.gcid
        }
      }).success(data => {
        data.forEach(item => {
          item.score = 0
        })
        this.stage = data
        this.stageMark = true
        this.formatdata()
      }).fail(data => {
      }).default(() => {
      })
    },
    getGameStageScore () {
      Http.send({
        url: 'GameStageScore',
        data: {
          gcid: Communication.stage.gcid,
          student: Account.uid
        }
      }).success(data => {
        console.log(data)
        this.score = data
        this.scoreMark = true
        this.formatdata()
      }).fail(data => {
      }).default(() => {
      })
    },
    formatdata () {
      if (this.stageMark && this.scoreMark) {
        this.stage.forEach(item => {
          this.score.forEach(unit => {
            if (item.gsid === unit.stage.gsid) {
              item.score = unit.score
            }
          })
        })
        this.table = this.stage
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./stage.scss";
</style>
