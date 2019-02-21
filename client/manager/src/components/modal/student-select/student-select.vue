<template>
  <!-- s  -->
  <section class="student-select">
    <div class="select-header">
      <p class="header-title">选择学员</p>
      <SearchBarComponent @SEARCH_EVENT="search" :placeholder="'请输入姓名'" :notNeedRefresh="true"></SearchBarComponent>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="select-content">
      <ul class="content-list">
        <li class="list-item fl" v-for="(item, index) in table" :key="index" @click="select(item, index)">
          <div class="item-warp" :class="{'selected': item.selected}">
            <img class="warp-portrait" src="">
            <p class="warp-name">{{item.detail.realname}}</p>
            <p class="warp-phone">{{item.phone}}</p>
            <!-- <p class="warp-school">{{getCollege(item.detail)}}</p> -->
          </div>
        </li>
      </ul>
    </div>
    <section class="select-operation" v-show="mode">
      <button class="btns-confirm" @click="confirm">确认</button>
      <button class="btns-cancel" @click="cancel">取消</button>
    </section>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
// import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'
import SearchBarComponent from '../../../../dependencies/components/search-bar/search-bar.vue'
import BtnComponent from '../../../../dependencies/components/btn/btn.vue'

export default {
  name: 'StudentSelectModalComponent',
  data () {
    return {
      students: [],
      table: [],
      content: {},
      mode: false,
      // start datas
      btn: {
        type: 'operation'
      }
      // end datas
    }
  },
  components: {
    // include chunk
    SearchBarComponent,
    BtnComponent
  },
  created () {
    this.getStudentList()
    if (Communication.panel.page === 'add-enroll') {
      this.mode = true
      this.select = this.multipleSelect
    } else if (Communication.panel.page === 'update-enroll') {
      this.mode = false
      this.select = this.singleSelect
    }
  },
  methods: {
    confirm () {
      Communication.modal = Object.values(this.content)
      this.cancel()
    },
    cancel () {
      Display.modal = false
    },
    select (item, index) {},
    multipleSelect (item, index) {
      this.$set(this.table[index], 'selected', !item.selected)
      item.selected ? this.content[item.user] = item : delete this.content[item.user]
    },
    singleSelect (item, index) {
      Communication.modal = item
      this.cancel()
    },
    search (keywords) {
      let table = []
      this.students.forEach(item => {
        if (item.detail.realname.indexOf(keywords) !== -1) table.push(item)
      })
      this.table = table
    },
    getStudentList () {
      Http.send({
        url: 'StudentList'
      }).success(data => {
        this.students = data
        this.table = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./student-select.scss";
</style>
