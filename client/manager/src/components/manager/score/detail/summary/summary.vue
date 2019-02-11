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
    <!-- <p class="detail-valuation" v-show="!evaluate">
      <span class="fz-24">评语：</span>
      <span class="fz-18">{{comment}}</span>
    </p>
    <div class="detail-comment" v-show="evaluate">
      <p class="comment-title fz-24 color-dark">
        <i></i>
        <span>评语：</span>
      </p>
      <textarea class="comment-input fz-18" v-model="comment"></textarea>
    </div>
    <div class="detail-btns">
      <button class="btn btn-submit fz-15 color-white" v-show="evaluate" @click="submitComment">
        <div>提交</div>
      </button>
      <button class="btn btn-update fz-15 color-white" v-show="!evaluate" @click="updateEdit">
        <div>更新</div>
      </button>
    </div> -->
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

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
    console.log(Communication.detail)
    // this.getScore()
    this.formatData({...Communication.detail})
    // this.getComment()
    // this.init()
  },
  methods: {
    // submitComment () {
    //   this.evaluate = false
    //   if (this.commentId !== '') {
    //     Http.send({
    //       url: 'UpdateComment',
    //       data: {
    //         comment: this.commentId,
    //         content: this.comment
    //       }
    //     }).success(data => {
    //     }).fail(data => {
    //       console.log(data)
    //     })
    //   } else {
    //     Http.send({
    //       url: 'AddComment',
    //       data: {
    //         hid: Communication.detail.hid,
    //         homework: Communication.detail.hid,
    //         sid: Communication.detail.id,
    //         student: Communication.detail.student,
    //         tid: Account.upid,
    //         content: this.comment
    //       }
    //     }).success(data => {
    //       this.getComment()
    //     }).fail(data => {
    //       console.log(data)
    //     })
    //   }
    // },
    // getComment () {
    //   Http.send({
    //     url: 'CommentSingle',
    //     data: {
    //       hid: Communication.detail.hid,
    //       sid: Communication.detail.id,
    //       student: Communication.detail.student,
    //       tid: Account.upid
    //     }
    //   }).success(data => {
    //     if (data.length) {
    //       this.comment = data[0].content
    //       this.commentId = data[0].comment
    //     }
    //   }).fail(data => {
    //     console.log(data)
    //   })
    // },
    // updateEdit () {
    //   this.evaluate = true
    // },
    getScore () {
      Http.send({
        url: 'GameStageScore',
        data: {
          student: Communication.detail.student,
          gcid: Communication.detail.gcid
        }
      }).success(data => {
      }).fail(data => {
        console.log(data)
      })
    },
    formatData (data) {
      let sum = 0
      let max = 0

      let content = []
      console.log(data.gsid[0])
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
