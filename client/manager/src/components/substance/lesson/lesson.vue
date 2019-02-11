<template>
  <!-- s  -->
  <section class="lesson">
    <div class="lesson-header">
      <div class="header-nav">课程内容</div>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="lesson-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-70">操作</th>
          <th class="table-70">序号</th>
          <th class="table-110">名称</th>
          <th class="table-130">创建人</th>
          <th class="table-210">描述</th>
          <th class="table-70">编号</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
            <td class="table-70">
              <button class="content-show-detail" :disabled="!item.enable" @click="showExample(item)">详情</button>
            </td>
            <td class="table-70">{{index + 1}}</td>
            <td class="table-110" :title="item.name">{{item.name}}</td>
            <td class="table-130">{{item.creater.name}}（{{item.creater.phone}}）</td>
            <td class="table-210">{{item.description}}</td>
            <td class="table-70">{{item.lid}}</td>
          </tr>
        </table>
      </div>
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
  name: 'LessonSubstanceComponent',
  data () {
    return {
      table: []
      // start datas
      // end datas
    }
  },
  created () {
    this.getLessonList()
  },
  methods: {
    getLessonList () {
      Http.send({
        url: 'LessonList',
        data: {
          cid: Communication.substance.course
        }
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
      })
    },
    showExample (item) {
      item.oid = Communication.substance.cls
      Communication.cview = item
      Display.cview = 'example'
    },
    cancel () {
      Display.substance = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./lesson.scss";
</style>
