<template>
  <!-- s  -->
  <section class="example">
    <div class="example-header">
      <div class="header-nav">课时内容</div>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="example-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-70">序号</th>
          <th class="table-90">游戏</th>
          <th class="table-90">章节</th>
          <th class="table-70">顺序</th>
          <th class="table-70">解锁</th>
          <th class="table-70">内容</th>
          <th class="table-70">编号</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
            <td class="table-70">{{index + 1}}</td>
            <td class="table-90">{{GameModule[item.gametype]}}</td>
            <td class="table-90" :title="item.detail.chapter">{{item.detail.chapter}}</td>
            <td class="table-70">{{item.idx}}</td>
            <td class="table-70">
              <button class="content-show-detail" :disabled="!item.enable" @click="refreshStatus(item, index)">{{item.unlock ? '已打开' : '已锁住'}}</button>
            </td>
            <td class="table-70">
              <button class="content-show-detail" :disabled="!item.enable" @click="gotoPage(item)">跳转</button>
            </td>
            <td class="table-70">{{item.leid}}</td>
          </tr>
        </table>
      </div>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'

export default {
  name: 'ExampleCviewComponent',
  data () {
    return {
      detail: Communication.cview,
      GameModule: Dictionary.Game,
      table: []
      // start datas
      // end datas
    }
  },
  created () {
    this.getExampleList()
  },
  methods: {
    init () {
      this.table.forEach(item => {
        this.getUnlock(item)
      })
    },
    gotoPage (item) {
      let url = `${window.gameUrl}?`
      url += `gcid=${item.gcid}&`
      url += `token=${Account.token}&`
      url += `user=${Account.uid}&`
      url += `origin=teacher&`
      url += `time=${(new Date()).getTime()}`
      window.open(url, 'game')
    },
    refreshStatus (item, index) {
      Http.send({
        url: 'GameStageOpenChapter',
        data: {
          oid: this.detail.oid,
          gcid: item.gcid
        }
      }).before(() => {
      }).success(data => {
        item.unlock = data
        this.table = [...this.table]
      }).fail(data => {
      }).default(() => {
      })
    },
    getUnlock (item) {
      Http.send({
        url: 'GameStageIsUnlock',
        data: {
          oid: this.detail.oid,
          gcid: item.gcid
        }
      }).before(() => {
      }).success(data => {
        item.unlock = data
        this.table = [...this.table]
      }).fail(data => {
      }).default(() => {
      })
    },
    getExampleList () {
      Http.send({
        url: 'ExampleList',
        data: {
          lid: this.detail.lid,
          enable: 2
        }
      }).before(() => {
      }).success(data => {
        console.log(data)
        this.table = data
        this.init()
      }).fail(data => {
      }).default(() => {
      })
    },
    cancel () {
      Display.cview = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./example.scss";
</style>
