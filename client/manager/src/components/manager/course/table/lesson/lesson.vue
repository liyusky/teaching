<template>
  <!-- s  -->
  <section class="lesson">
    <table class="lesson-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70" v-if="setPermission()">修改</th>
        <th class="table-70">序号</th>
        <th class="table-110">名称</th>
        <th class="table-130">创建人</th>
        <th class="table-210">描述</th>
        <th class="table-70" v-if="setPermission()">启用</th>
        <th class="table-70">编号</th>
      </tr>
    </table>
    <div class="lesson-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
          <td class="table-70">
            <button class="content-show-detail" :disabled="!item.enable" @click="showExample(item)">详情</button>
          </td>
          <td class="table-70" v-if="setPermission()">
            <button class="content-show-detail" :disabled="!item.enable" @click="updateLesson(item)">修改</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-110">{{item.name}}</td>
          <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
          <td class="table-210">{{item.description}}</td>
          <td class="table-70" v-if="setPermission()">
            <button class="content-btn" :disabled="item.disabled" @click="forbid(item, index)">
              <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
            </button>
          </td>
          <td class="table-70">{{item.lid}}</td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'
import Account from '../../../../../../dependencies/modules/Account.class.js'

export default {
  name: 'LessonTableComponent',
  props: ['table'],
  data () {
    return {
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
    showExample (item) {
      item.course = Communication.detail.name
      Communication.content = item
      Display.content = 'example'
    },
    forbid (item, index) {
      Http.send({
        url: 'UpdateLesson',
        data: {
          lid: item.lid,
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
    updateLesson (item) {
      Communication.panel = item
      Display.panel = 'lesson-update-lesson'
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./lesson.scss";
</style>
