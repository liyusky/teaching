<template>
  <!-- s  -->
  <section class="user">
    <div class="user-nav">
      <SearchBarComponent></SearchBarComponent>
      <div class="nav-btns">
        <BtnComponent :setting="btn" @BTN_CLICK_EVENT="refresh" class="btns-item">
          <i></i>
          <span>设为学生</span>
        </BtnComponent>
        <BtnComponent :setting="btn" @BTN_CLICK_EVENT="refresh" class="btns-item">
          <i></i>
          <span>设为教师</span>
        </BtnComponent>
      </div>
    </div>
    <section class="user-table">
      <table class="table-header table-reset">
        <tr>
          <th class="table-70">序号</th>
          <th class="table-110">名称</th>
          <th class="table-130">教师</th>
          <th class="table-210">描述</th>
          <th class="table-70">教学案例</th>
          <th class="table-70">作业</th>
          <th class="table-70">编号</th>
        </tr>
      </table>
      <div class="table-content">
        <table class="table-reset">
          <tr v-for="(item, index) in table" :key="index" :class="{'table-content-disable': !item.enable}">
            <td class="table-70">{{index + 1}}</td>
            <td class="table-110">{{item.name}}</td>
            <td class="table-130">{{teacher}}</td>
            <td class="table-210">{{item.description}}</td>
            <td class="table-70">
              <button class="content-show-detail" :disabled="!item.example" @click="showExample(item)">{{item.example ? '查看' : '暂无'}}</button>
            </td>
            <td class="table-70">
              <button class="content-show-detail" :disabled="!item.homework" @click="showHomework(item)">{{item.homework ? '查看' : '暂无'}}</button>
            </td>
            <td class="table-70">{{item.lid}}</td>
          </tr>
        </table>
      </div>
    </section>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
export default {
  name: 'UserComponent',
  data () {
    return {
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
@import "./user.scss";
</style>
