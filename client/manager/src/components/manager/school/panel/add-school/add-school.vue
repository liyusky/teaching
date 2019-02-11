<template>
  <!-- s  -->
  <section class="add-school">
    <div class="school-header">
      <p class="header-title">添加学校</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <div class="school-operation">
      <ul class="operation-setting-list">
        <li class="list-item">
          <label class="item-label" for="school-setting-add-name">学校：</label>
          <input class="item-input" id="school-setting-add-name" type="text" v-model="name" placeholder="请输入学校">
        </li>
        <li class="list-item">
          <label class="item-label" for="school-setting-add-district">校区：</label>
          <input class="item-input" id="school-setting-add-district" type="text" v-model="district" placeholder="请输入校区">
        </li>
        <li class="list-item">
          <label class="item-label" for="school-setting-add-school">年级：</label>
          <select class="item-select" id="school-setting-add-school" v-model="level">
            <option value="2" selected>小学</option>
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
  name: 'SchoolAddSchoolPanelComponent',
  data () {
    return {
      name: '',
      district: '',
      level: 2
      // start datas
      // end datas
    }
  },
  methods: {
    confirm () {
      if (!Check.appellation(this.name)) return
      let data = {
        name: this.name,
        level: this.level
      }
      if (this.district) {
        if (!Check.appellation(this.district)) return
        data.district = this.district
      }
      Http.send({
        url: 'AddSchool',
        data: data
      }).success(data => {
        Display.api = 'SchoolList'
      }).fail(data => {
      }).default(() => {
        this.confirmDisabled = false
        this.cancel()
      })
    },
    cancel () {
      if (Display.tip === 'school-add-school') Display.tip = false
      if (Display.panel === 'school-add-school') Display.panel = false
      Communication.modal = false
      this.clear()
    },
    clear () {
      this.name = ''
      this.district = ''
      this.level = 2
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./add-school.scss";
</style>
