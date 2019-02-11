<template>
  <!-- s  -->
  <section class="user-select">
    <div class="select-header">
      <p class="header-title">选择用户</p>
      <div class="header-close" @click="cancel">
        <i>x</i>
      </div>
    </div>
    <ul class="select-list">
      <li class="list-item fl" v-for="(item, index) in user" :key="index" @click="select(item)">
        <div class="item-warp">
          <img class="warp-portrait" src="">
          <p class="warp-name">{{item.name}}</p>
          <p class="warp-phone">{{item.phone}}</p>
          <!-- <p class="warp-school">{{getCollege(item.detail)}}</p> -->
          <select class="warp-role" v-model="role">
            <option value="1" selected>教学老师</option>
            <option value="2">教务老师</option>
            <option value="3">教务主任</option>
            <option value="4">教学主任</option>
            <option value="99">管理员</option>
          </select>
          <div class="warp-checkbox"></div>
          <input class="warp-checkbox" type="checkbox" >
        </div>
      </li>
    </ul>
    <section class="select-operation-btns">
      <button class="btns-confirm" :disabled="confirmDisabled" @click="confirm">确认</button>
      <button class="btns-cancel" v-show="allow" @click="cancel">取消</button>
    </section>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
export default {
  name: 'UserSelectComponent',
  data () {
    return {
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  methods: {
    // getCollege (detail) {
    //   if ('college' in detail) {
    //     return `${detail.college.name}${detail.college.district && detail.college.district !== 'null' ? detail.college.district : ''}${Dictionary.rank[detail.college.level]}`
    //   } else {
    //     return '未设置'
    //   }
    // },
    cancel () {
      Display.modal = false
    },
    select (item) {
      Communication.modal = item
      this.cancel()
    },
    getStudentList () {
      Http.send({
        url: 'StudentList'
      }).success(data => {
        this.students = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    }
  },
}
</script>

<style lang="sass" scoped>
@import "./user-select.scss";
</style>
