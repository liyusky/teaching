<template>
  <!-- s  -->
  <section class="problem">
    <div class="problem-header">
      <p class="header-title">添加作业内容</p>
      <div class="header-close" @click="closePanel">
        <i>x</i>
      </div>
    </div>
    <div class="problem-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="course-setting-chapter-name">名称：</label>
          <input class="item-input" id="course-setting-chapter-name" type="text">
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-chapter-knowledge">学校：</label>
          <input class="item-input" id="course-setting-chapter-knowledge" type="text">
        </li>
        <li class="list-item">
          <label class="item-label" for="setting-class-enroll-date">开始时间：</label>
          <div class="item-date" id="setting-class-enroll-date">2018-12-6 10:09:46</div>
        </li>
        <li class="list-item">
          <label class="item-label" for="setting-class-enroll-date">结束时间：</label>
          <div class="item-date" id="setting-class-enroll-date">2018-12-6 10:09:46</div>
        </li>
        <li class="list-item">
          <label class="item-label" for="course-setting-chapter-remarks">描述：</label>
          <textarea class="item-textarea" id="course-setting-chapter-remarks"></textarea>
        </li>
      </ul>
      <BtnComponent class="operation-btns" :setting="btn"></BtnComponent>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Display from '../../../../../../dependencies/modules/Display.class.js'
import BtnComponent from '../../../../../../dependencies/components/btn/btn.vue'
export default {
  name: 'HomeworkAddProblemPanelComponent',
  data () {
    return {
      // start datas
      btn: {
        type: 'operation'
      }
      // end datas
    }
  },
  components: {
    BtnComponent
    // include chunk
  },
  methods: {
    closePanel () {
      Display.panel = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./problem.scss";
</style>
