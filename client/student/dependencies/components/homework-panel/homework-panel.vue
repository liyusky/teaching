<template>
  <!-- s  -->
  <section class="homework-panel">
    <div class="panel-header">
      <div class="panel-title">{{homeworkPanel.title}}</div>
      <button class="panel-refresh" @click="refreshStatus">刷新</button>
    </div>
    <table>
      <tr>
        <th>标题</th>
        <th>游戏</th>
        <th>通关</th>
        <th>详情</th>
      </tr>
      <tbody class="border-1">
        <tr v-for="(item, index) in score" :key="index">
          <td>{{item.detail.chapter}}</td>
          <td>
            <button class="detail-btn color-white" :class="{'bg-grey': !item.unlock}" :disabled="!item.unlock" @click="gotoPage(item)">{{item.unlock ? '跳转' : '已锁'}}</button>
          </td>
          <th>{{item.finish ? '已完成' : '未完成'}}</th>
          <td>
            <button class="detail-btn color-white" :class="{'bg-grey': !item.unlock}" :disabled="!item.unlock" @click="showStage(item)">
              <div>{{item.unlock ? '查看' : '已锁'}}</div>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../modules/Account.class.js'
import Communication from '../../modules/Communication.class.js'
import Http from '../../modules/Http.class.js'
import Router from '../../modules/Router.class.js'

export default {
  name: 'HomeworkPanelComponent',
  props: ['homeworkPanel'],
  data () {
    return {
      score: this.homeworkPanel.score,
      url: '',
      count: 0,
    }
  },
  created () {
    this.refreshStatus()
    console.log(this.$route.name)
  },
  methods: {
    showStage (item) {
      Communication.stage = item
      switch (this.$route.name) {
        case 'student-example':
          Router.push(`student-example-stage`)
          break
        case 'student-homework':
          Router.push(`student-homework-stage`)
          break
      }
    },
    gotoPage (item) {
      let url = `${window.gameUrl}?`
      url += `gcid=${item.gcid}&`
      url += `token=${Account.token}&`
      url += `user=${Account.uid}&`
      url += `origin=student&`
      url += `time=${(new Date()).getTime()}`
      window.open(url, 'game')
    },
    refreshStatus () {
      this.count = 0
      let newScore = [...this.score]
      newScore.forEach((item, index) => {
        Http.send({
          url: 'GameStageIsFinished',
          data: {
            gcid: item.gcid,
            student: Account.uid
          }
        }).success(data => {
          item.finish = data
          this.count += 1
          this.score = [...newScore]
        }).fail(data => {
          console.log(data)
        })
        Http.send({
          url: 'GameStageIsUnlock',
          data: {
            gcid: item.gcid,
            student: Account.uid
          }
        }).success(data => {
          item.unlock = data
          this.score = [...newScore]
        }).fail(data => {
          console.log(data)
        })
      })
    }
  },
  watch: {
    count (value) {
      this.$emit('REFRESH_SCHEDULE_EVENT', value)
    }
  },
}
</script>

<style lang="sass" scoped>
@import "./homework-panel.scss";
</style>
