<template>
  <!-- s  -->
  <section class="game-chapter-select">
    <div class="select-header">
      <p class="header-title">选择游戏章节</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="select-list">
        <li class="list-item fl" v-for="(item, index) in chapter" :key="index" @click="select(item)">
          <div class="item-wrap">
            <div class="wrap-message" :title="item.title">{{item.title}}</div>
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
  name: 'GameChapterSelectModalComponent',
  data () {
    return {
      gametype: 0,
      gcid: 0,
      gsid: 0,
      chapter: []
      // start datas
      // end datas
    }
  },
  created () {
    this.gametype = Communication.modal
    this.getGameChapterList()
  },
  methods: {
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getGameChapterList () {
      Http.send({
        url: 'GameChapterList',
        data: {
          gametype: this.gametype
        }
      }).success(data => {
        this.chapter = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./game-chapter-select.scss";
</style>
