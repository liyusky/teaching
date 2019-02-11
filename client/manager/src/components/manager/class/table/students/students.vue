<template>
  <!-- s  -->
  <section class="students">
    <table class="students-header">
      <tr>
        <th class="table-70">序号</th>
        <th class="table-70">姓名</th>
        <th class="table-100">手机号</th>
        <!-- <th class="table-150">学校</th> -->
        <th class="table-130">报名时间</th>
        <th class="table-70">退班</th>
        <th class="table-70">结业</th>
        <th class="table-70">缴费</th>
        <th class="table-70">启用</th>
      </tr>
    </table>
    <div class="students-content">
      <table>
        <tr :class="{'table-content-disable': !item.enable}" v-for="(item, index) in table" :key="index">
          <td class="table-70">{{index + 1}}</td>
          <td class="table-70">{{item.name}}</td>
          <td class="table-100">{{item.phone}}</td>
          <!-- <td class="table-150">{{item.school}}{{item.district}}</td> -->
          <td class="table-130">{{item.enrollDate}}</td>
          <td class="table-70">
            <button class="content-show-detail">退班</button>
          </td>
          <td class="table-70">
            <button class="content-show-detail">结业</button>
          </td>
          <td class="table-70">
            <button class="content-show-detail">查看</button>
          </td>
          <td class="table-70">
            <i class="iconfont" :class="item.enable ? 'icon-tick': 'icon-cross'"></i>
          </td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
export default {
  name: 'StudentsTableComponent',
  data () {
    return {
      table: [
        {
          sid: 1,
          name: '周芷若',
          phone: '15921769360',
          // school: '石化一中',
          district: '南区',
          enrollDate: '2018-10-1',
          enable: true
        },
        {
          sid: 2,
          name: '周芷若',
          phone: '15921769360',
          // school: '石化一中',
          district: '南区',
          enrollDate: '2018-10-1',
          enable: false
        }
      ]
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  }
}
</script>

<style lang="sass" scoped>
@import "./students.scss";
</style>
