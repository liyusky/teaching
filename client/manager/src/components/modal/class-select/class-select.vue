<template>
  <!-- s  -->
  <section class="class-select">
    <div class="select-header">
      <p class="header-title">选择班级</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="select-list">
        <li class="list-item fl" v-for="(item, index) in organization" :key="index" @click="select(item)">
          <div class="item-wrap">
            <img class="wrap-portrait" src="">
            <div class="wrap-message">
              <p class="message-name">{{item.name}}</p>
              <p class="message-tip">{{item.manager.name}}（{{item.manager.phone}}）</p>
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
  name: 'ClassSelectModalComponent',
  data () {
    return {
      organization: []
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  created () {
    this.getClassList()
  },
  methods: {
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getClassList () {
      Http.send({
        url: 'ClassList'
      }).success(data => {
        this.organization = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./class-select.scss";
</style>
