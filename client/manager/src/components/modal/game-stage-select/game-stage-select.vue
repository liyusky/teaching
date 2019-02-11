<template>
  <!-- s  -->
  <section class="game-stage-select">
    <div class="select-header">
      <p class="header-title">选择游戏场景</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="select-list">
        <li class="list-item fl" v-for="(item, index) in stages" :key="index" @click="select(item)">
          <div class="item-wrap">
            <div class="wrap-message">{{item.name}}</div>
          </div>
        </li>
      </ul>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'

export default {
  name: 'GameStageSelectModalComponent',
  data () {
    return {
      gametype: 0,
      gcid: 0,
      stages: []
      // start datas
      // end datas
    }
  },
  created () {
    let modal = {...Communication.modal}
    this.gametype = modal.gametype
    this.gcid = modal.gcid
    console.log(this.gametype)
    console.log(this.gcid)
    this.getGameStageList()
  },
  methods: {
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getGameStageList () {
      Http.send({
        url: 'GameStageList',
        data: {
          gametype: this.gametype,
          gcid: this.gcid
        }
      }).success(data => {
        this.stages = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./game-stage-select.scss";
</style>
