<template>
  <!-- s  -->
  <section class="add-example">
    <div class="example-header">
      <p class="header-title">
        <span class="title-name">添加教学案例</span>
      </p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="example-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="example-setting-add-type">游戏类型：</label>
          <select class="item-select" id="example-setting-add-type" v-model="gametype">
            <option value="0">酷町猫</option>
            <option value="1">酷町打字</option>
          </select>
        </li>
        <li class="list-item">
          <label class="item-label" for="example-setting-add-game-stage">游戏章节：</label>
          <input class="item-input" id="example-setting-add-game-stage" type="text" readonly="readonly" v-model="gameChapter" @click="selectGameChapter">
        </li>
        <!-- <li class="list-item">
          <label class="item-label" for="example-setting-add-game-chapter">章节关卡：</label>
          <input class="item-input" id="example-setting-add-game-chapter" type="text" readonly="readonly" v-model="gameStage" @click="selectGameStage">
        </li> -->
        <li class="list-item">
          <label class="item-label" for="example-setting-add-index">顺序：</label>
          <select class="item-select" id="example-setting-add-index" v-model="index">
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
  name: 'ExampleAddExamplePanelComponent',
  data () {
    return {
      lid: Communication.panel,
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
    console.log(Communication.panel)
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
      Http.send({
        url: 'AddExample',
        data: {
          lid: this.lid,
          lesson: this.lid,
          gametype: this.gametype,
          gcid: this.gcid,
          // gsid: this.gsid,
          idx: this.index
        }
      }).success(data => {
        Display.api = 'ExampleList'
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
@import "./add-example.scss";
</style>
