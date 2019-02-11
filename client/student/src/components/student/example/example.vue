<template>
  <!-- s  -->
  <section class="example">
    <div class="detail-statistics">
      <div class="statistics-tip">教学案例完成度</div>
      <div class="statistics-schedule">
        <ScheduleComponent :schedule="schedule"></ScheduleComponent>
      </div>
    </div>
    <div class="detail-content">
      <HomeworkPanelComponent v-for="(item, index) in homeworkPanel" :key="index" :homeworkPanel="item" @REFRESH_SCHEDULE_EVENT="refreshSchedule"></HomeworkPanelComponent>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../../../dependencies/modules/Account.class.js'
import Communication from '../../../../dependencies/modules/Communication.class.js'
// import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'
import HomeworkPanelComponent from '../../../../dependencies/components/homework-panel/homework-panel.vue'
import ScheduleComponent from '../../../../dependencies/components/schedule/schedule.vue'
export default {
  name: 'ExampleComponent',
  data () {
    return {
      comment: '',
      homeworkPanel: [],
      schedule: 100,
      max: 0
      // start params
      // end params
    }
  },
  components: {
    HomeworkPanelComponent,
    ScheduleComponent
    // include components
  },
  created () {
    Account.logout()
    this.getScoreList()
    // this.getComment()
  },
  methods: {
    getScoreList () {
      Http.send({
        url: 'ExampleScoreList',
        data: {
          lid: Communication.example.lid,
          student: Account.uid
        }
      }).success(data => {
        this.homeworkPanel = this.formatData(data)
        this.max = data.length
      }).fail(data => {
      })
    },
    // getComment () {
    //   Http.send({
    //     url: 'CommentSingle',
    //     data: {
    //       hid: Communication.example.hid,
    //       sid: Account.upid,
    //       student: Account.uid
    //     }
    //   }).success(data => {
    //     if (data.length) {
    //       this.comment = data[0].content
    //     }
    //   }).fail(data => {
    //     console.log(data)
    //   })
    // },
    formatData (data) {
      let arr = []
      let content = {
        title: '酷町猫',
        score: []
      }
      data.forEach(item => {
        content.score.push(item)
      })
      arr.push(content)
      console.log(arr)

      return arr
    },
    refreshSchedule (value) {
      this.schedule = 100 * value / this.max
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./example.scss";
</style>
