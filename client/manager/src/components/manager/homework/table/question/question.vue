<template>
  <!-- s  -->
  <section class="question">
    <table class="question-header table-reset">
      <tr>
        <th class="table-70">修改</th>
        <th class="table-70">序号</th>
        <th class="table-90">游戏</th>
        <th class="table-110">章节</th>
        <!-- <th class="table-110">关卡</th> -->
        <th class="table-70">顺序</th>
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="question-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateQuestion(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-90">{{GameModule[item.gametype]}}</td>
          <td class="table-110" :title="item.detail.chapter">{{item.detail.chapter}}</td>
          <!-- <td class="table-110">{{item.detail.stage}}</td> -->
          <th class="table-70">{{item.idx}}</th>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.qid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'QuestionComponent',
  props: ['table'],
  data () {
    return {
      GameModule: Dictionary.Game
      // start datas
      // end datas
    }
  },
  methods: {
    forbid (item, index) {
      Http.send({
        url: 'UpdateQuestion',
        data: {
          qid: item.qid,
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
      item.hid = Communication.detail.hid
      Communication.panel = item
      Display.panel = 'question-update-question'
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./question.scss";
</style>
