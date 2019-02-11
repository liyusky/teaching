<template>
  <!-- s  -->
  <section class="update-school">
    <div class="school-header">
      <p class="header-title">修改学校</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="school-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="school-setting-update-name">学校：</label>
          <input class="item-input" id="school-setting-update-name" type="text" v-model="name" placeholder="请输入学校">
        </li>
        <li class="list-item">
          <label class="item-label" for="school-setting-update-district">校区：</label>
          <input class="item-input" id="school-setting-update-district" type="text" v-model="district" placeholder="请输入校区">
        </li>
        <li class="list-item">
          <label class="item-label" for="school-setting-update-school">年级：</label>
          <select class="item-select" id="school-setting-update-school" v-model="level">
            <option value="2">小学</option>
            <option value="3">初中</option>
            <option value="4">高中</option>
          </select>
        </li>
      </ul>
      <section class="operation-btns">
        <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
        <button class="btns-cancel" @click="cancel">取消</button>
      </section>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Check from '../../../../../../dependencies/modules/Check.class.js'
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'SchoolUpdateSchoolPanelComponent',
  data () {
    return {
      school: 0,
      name: '',
      district: '',
      level: 0,
      confirmDisabled: false
      // start datas
      // end datas
    }
  },
  created () {
    let panel = {...Communication.panel}
    this.data = {...Communication.panel}
    this.school = panel.school
    this.district = panel.district
    this.name = panel.name
    this.level = panel.level
  },
  methods: {
    confirm () {
      let data = {school: this.school}

      if (this.data.name !== this.name) {
        if (!Check.appellation(this.name)) return
        data.name = this.name
      }

      if (this.data.district !== this.district) {
        if (!Check.appellation(this.district)) return
        data.district = this.district
      }

      if (this.data.level !== this.level) data.level = this.level

      Http.send({
        url: 'UpdateSchool',
        data: data
      }).before(() => {
        this.confirmDisabled = true
      }).success(data => {
        Display.api = 'SchoolList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        Display.panel = false
      })
    },
    cancel () {
      Display.panel = false
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./update-school.scss";
</style>
