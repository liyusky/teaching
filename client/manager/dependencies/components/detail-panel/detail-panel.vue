<template>
  <!-- s 详情面板 -->
  <section class="detail-panel">
    <div class="panel-page">
      <div class="page-header">
        <div class="header-title">
          <div class="title-introduction">
            <p class="introduction-name">小猫打字班</p>
            <p class="introduction-tip">已有1人，上限30人</p>
          </div>
          <div class="title-adviser">
            <img class="adviser-portrait" src="">
            <div class="adviser-name">成龙</div>
          </div>
        </div>
        <div class="header-operation">
          <button class="operation-btn">学员报名</button>
          <button class="operation-btn">设置上课提醒时间</button>
          <button class="operation-btn">结业</button>
          <button class="operation-btn">编辑</button>
          <button class="operation-btn">删除</button>
        </div>
      </div>
      <nav class="page-nav">
        <div class="nav-item selected">班级课表</div>
        <div class="nav-item">班级学员</div>
      </nav>
      <div class="page-operation">
        <button class="operation-add">
          <i></i>
          <span>排课</span>
        </button>
        <div class="operation-choose-week">
          <button class="week-before">上一周</button>
          <button class="week-current">本周</button>
          <button class="week-affter">下一周</button>
        </div>
      </div>
      <table class="page-curriculum">
        <tr class="curriculum-header">
          <th>上课时间</th>
          <th>
            <p>星期一</p>
            <p>12月03日</p>
          </th>
          <th>
            <p>星期二</p>
            <p>12月04日</p>
          </th>
          <th>
            <p>星期三</p>
            <p>12月05日</p>
          </th>
          <th>
            <p>星期四</p>
            <p>12月06日</p>
          </th>
          <th>
            <p>星期五</p>
            <p>12月07日</p>
          </th>
          <th>
            <p>星期六</p>
            <p>12月08日</p>
          </th>
          <th>
            <p>星期日</p>
            <p>12月09日</p>
          </th>
        </tr>
        <tr class="curriculum-content">
          <td>8:00~9:00</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td rowspan="2">
            <p>刘亦菲</p>
            <p>神仙姐姐成长课</p>
          </td>
        </tr>
        <tr class="curriculum-content">
          <td>9:00~10:00</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr class="curriculum-content">
          <td>10:00~11:00</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr class="curriculum-content">
          <td>11:00~12:00</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr class="curriculum-content">
          <td>13:00~14:00</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr class="curriculum-content">
          <td>14:00~15:00</td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </table>
      <aside class="page-roll-back">
        <div class="back-sign">
          <i></i>
        </div>
      </aside>
    </div>
  </section>
  <!-- s 详情面板 -->
</template>

<script>// include dependence
export default {
  name: 'DetailPanelComponent',
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
@import "./detail-panel.scss";
</style>
