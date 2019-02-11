<template>
  <!-- s  -->
  <section class="update-example">
    <div class="example-header">
      <p class="header-title">
        <span class="title-main">修改教学案例</span>
        <span class="title-tip">（案例编号 {{leid}}）</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="example-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="question-setting-update-type">游戏类型：</label>
          <select class="item-select" id="question-setting-update-type" v-model="gametype">
            <option value="0">酷町猫</option>
            <option value="1">酷町打字</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="question-setting-update-game-stage">游戏章节：</label>
          <input class="item-input" id="question-setting-update-game-stage" type="text" readonly="readonly" v-model="gameChapter" @click="selectGameChapter">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="question-setting-update-game-chapter">章节关卡：</label>
          <input class="item-input" id="question-setting-update-game-chapter" type="text" readonly="readonly" v-model="gameStage" @click="selectGameStage">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="example-setting-update-index">顺序：</label>
          <select class="item-select" id="example-setting-update-index" v-model="index">
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
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'ExampleUpdateExamplePanelComponent',
  data () {
    return {
      leid: 0,
      gametype: 0,
      gcid: 0,
      gsid: 0,
      index: 1,
      gameStage: '',
      gameChapter: '',
      data: {},
      memory: [
        {
          gsid: 0,
          gcid: 0,
          gameStage: '',
          gameChapter: ''
        },
        {
          gsid: 0,
          gcid: 0,
          gameStage: '',
          gameChapter: ''
        }
      ],
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  created () {
    console.log(Communication.panel)
    let panel = {...Communication.panel}
    this.data = {
      gsid: panel.gsid,
      gcid: panel.gcid,
      leid: panel.leid,
      idx: panel.idx,
      lid: panel.lesson,
      gametype: panel.gametype * 1
    }
    this.gametype = panel.gametype
    this.gsid = panel.gsid
    this.gcid = panel.gcid
    this.leid = panel.leid
    this.index = panel.idx
    this.gameStage = panel.detail.stage
    this.gameChapter = panel.detail.chapter
    this.memory[this.gametype].gsid = panel.gsid
    this.memory[this.gametype].gcid = panel.gcid
    this.memory[this.gametype].gameStage = panel.detail.stage
    this.memory[this.gametype].gameChapter = panel.detail.chapter
  },
  methods: {
    selectGameChapter () {
      Communication.modal = this.gametype
      Display.modal = 'game-chapter-select'
    },
    selectGameStage () {
      if (this.gcid > 0) {
        alert('已选择章节，章节与关卡直能选其一')
        return
      }
      Communication.modal = {
        gametype: this.gametype,
        gcid: this.gcid
      }
      Display.modal = 'game-stage-select'
    },
    confirm () {
      let data = {
        leid: this.leid,
        lid: this.data.lid
      }

      if (this.data.gametype !== this.gametype) data.gametype = this.gametype
      if (this.data.idx !== this.index) data.idx = this.index
      // if (this.data.gsid !== this.gsid) data.gsid = this.gsid
      if (this.data.gcid !== this.gcid) data.gcid = this.gcid

      Http.send({
        url: 'UpdateExample',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'ExampleList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
    }
  },
  watch: {
    gametype (current, previous) {
      if (current !== previous) {
        this.gsid = this.memory[current].gsid
        this.gcid = this.memory[current].gcid
        this.gameStage = this.memory[current].gameStage
        this.gameChapter = this.memory[current].gameChapter
      }
    },
    gcid (current, previous) {
      if (current !== previous) {
        if (current !== this.memory[this.gametype].gcid) {
          this.gsid = 0
          this.gameStage = ''
        } else {
          this.gsid = this.memory[this.gametype].gsid
          this.gameStage = this.memory[this.gametype].gameStage
        }
      }
      this.memory[this.gametype].gcid = this.gcid
      this.memory[this.gametype].gameChapter = this.gameChapter
    },
    '$store.state.modal' (modal, previous) {
      if (previous === 'game-stage-select' && modal === false && Communication.modal) {
        this.gameStage = Communication.modal.name
        this.gsid = {...Communication.modal}.gsid
        this.memory[this.gametype].gsid = this.gsid
        this.memory[this.gametype].gameStage = this.gameStage
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
@import "./update-example.scss";
</style>
