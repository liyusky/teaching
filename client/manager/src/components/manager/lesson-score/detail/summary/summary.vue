<template>
  <!-- s  -->
  <section class="summary">
    <div class="summary-statistics">
      <div class="statistics-tip">作业完成度</div>
      <div class="statistics-schedule">
        <div class="schedule">
          <div class="schedule-line" :style="{width: schedule + '%'}"></div>
          <div class="schedule-num">{{schedule}}%</div>
        </div>
      </div>
    </div>
    <div class="detail-content">
      <div class="content-panel">
        <div class="panel-title">酷町猫</div>
        <table class="table-reset">
          <tr>
            <th>关卡</th>
            <th>得分</th>
          </tr>
          <tbody class="border-1">
            <tr v-for="(game, index) in content" :key="index">
              <td>{{game.stage}}</td>
              <td>{{game.score}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'

export default {
  name: 'SummaryComponent',
  data () {
    return {
      evaluate: true,
      comment: '',
      commentId: '',
      content: [],
      schedule: 100
    }
  },
  components: {
    // include components
  },
  created () {
    this.formatData({...Communication.detail})
  },
  methods: {
    formatData (data) {
      let sum = 0
      let max = 0

      let content = []
      let gisdss = data.gsid
      let scoress = data.score
      let stagess = data.stage
      data.stage.forEach((item, index) => {
        content.push({
          gsid: gisdss[index],
          score: scoress[index],
          stage: stagess[index]
        })
        sum += (scoress[index] || 0)
        max += 1
      })
      this.content = content
      this.schedule = sum / max
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./summary.scss";
</style>
