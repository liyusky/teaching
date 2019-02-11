<template>
  <!-- s  -->
  <div class="schedule">
    <div class="schedule-rail">
      <div class="rail-line" :style="{width: schedule + '%'}"></div>
      <div class="rail-num">{{schedule}}%</div>
    </div>
  </div>
  <!-- s  -->
</template>

<script>
export default {
  name: 'ScheduleComponent',
  props: ['schedule'],
  data () {
    return {
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./schedule.scss";
</style>
