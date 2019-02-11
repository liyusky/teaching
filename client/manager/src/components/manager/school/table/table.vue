<template>
  <!-- s  -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">序号</th>
        <th class="table-130">学校</th>
        <th class="table-110">校区</th>
        <th class="table-100">年级</th>
        <th class="table-70">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="table-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateSchool(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-130">{{item.name}}</td>
          <td class="table-110">{{item.district ? item.district : '无'}}</td>
          <td class="table-100">{{item.level ? DictionaryModule.rank[item.level] : '无'}}</td>
          <td class="table-70">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont">X</i>
            </button>
          </td>
          <td class="table-70">{{item.school}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'SchoolTableComponent',
  data () {
    return {
      table: [],
      DictionaryModule: Dictionary
      // start datas
      // end datas
    }
  },
  created () {
    this.getSchoolList()
  },
  methods: {
    getSchoolList () {
      Http.send({
        url: 'SchoolList',
        data: {
          enable: 2
        }
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateSchool',
        data: {
          school: item.school,
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
    updateSchool (item) {
      Communication.panel = item
      Display.panel = 'school-update-school'
    }
  },
  watch: {
    '$store.state.api' (api) {
      if (api === 'SchoolList') {
        this.getSchoolList()
        Display.api = false
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
