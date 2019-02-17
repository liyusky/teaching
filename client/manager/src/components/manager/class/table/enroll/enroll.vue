<template>
  <!-- s  -->
  <section class="enroll">
    <table class="enroll-header table-reset">
      <tr>
        <th class="table-70" v-if="setPermission()">操作</th>
        <th class="table-70">序号</th>
        <th class="table-110">姓名</th>
        <th class="table-70">状态</th>
        <th class="table-130" v-if="setPermission()">创建人</th>
        <th class="table-70" v-if="setPermission()">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="enroll-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70" v-if="setPermission()">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateEnroll(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110">{{item.studentDetail.name}}（{{item.studentDetail.phone}}）</td>
          <td class="table-70">{{DictionaryModule.status.student[item.status]}}</td>
          <td class="table-130" v-if="setPermission()">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-70" v-if="setPermission()">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.eid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Account from '../../../../../../dependencies/modules/Account.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'EnrollTableComponent',
  props: ['table'],
  data () {
    return {
      DictionaryModule: Dictionary
      // start datas
      // end datas
    }
  },
  methods: {
    setPermission () {
      let show = true
      if (Account.role < 99) show = false
      return show
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateEnroll',
        data: {
          eid: item.eid,
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
    updateEnroll (item) {
      Communication.panel = item
      Display.panel = 'enroll-update-enroll'
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./enroll.scss";
</style>
