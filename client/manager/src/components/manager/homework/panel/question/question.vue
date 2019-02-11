<template>
  <!-- s  -->
  <section class="question">
    <div class="question-header">
      <p class="header-title">
        <span class="title-name">添加问题</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="question-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="question-setting-add-type">游戏类型：</label>
          <select class="item-select" id="question-setting-add-type" v-model="gametype">
            <option value="0">酷町猫</option>
            <option value="1">酷町打字</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="question-setting-add-game-stage">游戏章节：</label>
          <input class="item-input" id="question-setting-add-game-stage" type="text" readonly="readonly" v-model="gameChapter" @click="selectGameChapter">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="question-setting-add-game-chapter">章节关卡：</label>
          <input class="item-input" id="question-setting-add-game-chapter" type="text" readonly="readonly" v-model="gameStage" @click="selectGameStage">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="question-setting-add-index">顺序：</label>
          <select class="item-select" id="question-setting-add-type" v-model="index">
            <option :value="index" v-for="index in 20" :key="index">{{index}}</option>
          </select>
        </li>
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
        <button class="btns-cancel" @click="cancel">取消</button>
      </section>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
// import Account from '../../../../../../dependencies/modules/Account.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'QuestionAddQuestionPanelComponent',
  data () {
    return {
      hid: 0,
      gametype: 0,
      gsid: 0,
      gcid: 0,
      gameStage: '',
      gameChapter: '',
      index: 1
      // start datas
      // end datas
    }
  },
  created () {
    this.hid = {...Communication.panel}.hid
  },
  methods: {
    selectGameChapter () {
      Communication.modal = this.gametype
      Display.modal = 'game-chapter-select'
    },
    selectGameStage () {
      if (this.gcid <= 0) {
        alert('请先选择章节')
        return
      }
      Communication.modal = {
        gametype: this.gametype,
        gcid: this.gcid
      }
      Display.modal = 'game-stage-select'
    },
    confirm () {
      if (!this.gcid) {
        alert('请选择章节')
        return
      }
      // if (!this.gsid) {
      //   alert('请选择关卡')
      //   return
      // }
      Http.send({
        url: 'AddQuestion',
        data: {
          hid: this.hid,
          homework: this.hid,
          gametype: this.gametype,
          gcid: this.gcid,
          // gsid: this.gsid,
          idx: this.index
        }
      }).success(data => {
        Display.api = 'QuestionList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        this.cancel()
      })
    },
    cancel () {
      Display.panel = false
      this.clear()
    },
    clear () {
      this.name = ''
      this.description = ''
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      if (previous === 'game-stage-select' && modal === false && Communication.modal) {
        this.gameStage = Communication.modal.name
        this.gsid = {...Communication.modal}.gsid
        Communication.modal = false
      } else if (previous === 'game-chapter-select' && modal === false && Communication.modal) {
        this.gameChapter = Communication.modal.title
        this.gcid = {...Communication.modal}.gcid
        Communication.modal = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./question.scss";
</style>
