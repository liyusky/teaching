<template>
  <!-- s  -->
  <section class="lesson-select">
    <div class="select-header">
      <p class="header-title">选择课时</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="select-list">
        <li class="list-item fl" v-for="(item, index) in lesson" :key="index" @click="select(item)">
          <div class="item-wrap">
            <img class="wrap-portrait" src="">
            <div class="wrap-message">
              <p class="message-name">{{item.name}}</p>
              <p class="message-tip">{{item.description}}</p>
            </div>
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
  name: 'LessonSelectModalComponent',
  data () {
    return {
      lesson: []
      // start datas
      // end datas
    }
  },
  created () {
    this.getLessonList()
  },
  methods: {
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getLessonList () {
      if (this.cid <= 0) return
      Http.send({
        url: 'LessonList',
        data: {
          cid: Communication.modal
        }
      }).success(data => {
        this.lesson = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./lesson-select.scss";
</style>
