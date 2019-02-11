<template>
  <!-- s  -->
  <section class="school-select">
    <div class="select-header">
      <p class="header-title">选择学校</p>
      <div class="header-level" :class="{'selected': level == 2}" @click="selectLevel(2)">小学</div>
      <div class="header-level" :class="{'selected': level == 3}" @click="selectLevel(3)">初中</div>
      <div class="header-level" :class="{'selected': level == 4}" @click="selectLevel(4)">高中</div>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="content-list">
        <li class="list-item fl" v-for="(item, index) in school" :key="index" @click="select(item)">
          <div class="item-wrap">
            <div class="wrap-message">{{item.name}}{{item.district}}</div>
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
  name: 'SchoolSelectModalComponent',
  data () {
    return {
      level: 4,
      school: []
      // start datas
      // end datas
    }
  },
  created () {
    this.getSchoolList()
  },
  methods: {
    selectLevel (level) {
      this.level = level
      this.getSchoolList()
    },
    cancel () {
      Display.modal = false
    },
    select (item) {
      console.log(item)
      Communication.modal = item
      this.cancel()
    },
    getSchoolList () {
      if (this.cid <= 0) return
      Http.send({
        url: 'SchoolList',
        data: {
          level: this.level,
          enable: 1
        }
      }).success(data => {
        this.school = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'SchoolList') {
        this.getSchoolList()
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./school-select.scss";
</style>
