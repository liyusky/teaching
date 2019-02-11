<template>
  <!-- s  -->
  <section class="example">
    <div class="example-header">
      <div class="header-nav">
        <div class="nav-introduction">
          <p class="introduction-name">{{detail.name}}</p>
          <p class="introduction-tip">课程：{{detail.course}}</p>
        </div>
        <button class="nav-btn" @click="addExample">添加案例</button>
      </div>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="example-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-70">修改</th>
          <th class="table-70">序号</th>
          <th class="table-90">游戏</th>
          <th class="table-90">章节</th>
          <th class="table-70">顺序</th>
          <th class="table-70">启用</th>
          <th class="table-70">编号</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
            <td class="table-70">
              <button class="content-show-detail" :disabled="!item.enable" @click="updateQuestion(item)">修改</button>
            </td>
            <td class="table-70">{{index + 1}}</td>
            <td class="table-90">{{GameModule[item.gametype]}}</td>
            <td class="table-90">{{item.detail.chapter}}</td>
            <td class="table-70">{{item.idx}}</td>
            <td class="table-70">
              <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
                <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
              </button>
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
import Http from '../../../../dependencies/modules/Http.class.js'

export default {
  name: 'ExampleContentComponent',
  data () {
    return {
      detail: Communication.content,
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
    getExampleList () {
      Http.send({
        url: 'ExampleList',
        data: {
          lid: this.detail.lid,
          enable: 2
        }
      }).before(() => {
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
      })
    },
    addExample () {
      Communication.panel = this.detail.lid
      Display.panel = 'example-add-example'
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateExample',
        data: {
          leid: item.leid,
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
    updateQuestion (item) {
      Communication.panel = item
      Display.panel = 'example-update-example'
    },
    cancel () {
      Display.content = false
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'ExampleList') {
        this.getExampleList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./example.scss";
</style>
