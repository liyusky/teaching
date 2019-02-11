<template>
  <!-- s 分页器 -->
  <section class="separator">
    <ul class="separator-list">
      <li class="list-first-page border" @click="firstPage">首页</li>
      <li class="list-pagination border" @click="leftMove">&lt;</li>
      <li class="list-pagination border">{{separator}}</li>
      <li class="list-pagination border">{{separator + 1}}</li>
      <li class="list-pagination border">{{separator + 2}}</li>
      <li class="list-pagination border">{{separator + 3}}</li>
      <li class="list-pagination border">{{separator + 4}}</li>
      <li class="list-pagination border" @click="rightMove">&gt;</li>
      <li class="list-last-page border" @click="lastPage">尾页</li>
      <li class="list-choose-number border">10条/页</li>
      <li class="list-target">
        <span>跳至</span>
        <input class="target-input border" type="number" :class="separatorTargetStatus">
        <span>页/共{{count}}页</span>
      </li>
    </ul>
  </section>
  <!-- s 分页器 -->
</template>

<script>
// include dependence
export default {
  name: 'SeparatorComponent',
  data () {
    return {
      separator: 11,
      count: 30
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
  },
  methods: {
    firstPage () {
      this.separator = 1
    },
    leftMove () {
      this.separator > 1 ? this.separator-- : (this.separator = 1)
    },
    rightMove () {
      (this.separator + 4) < this.count ? this.separator++ : (this.separator = this.count - 4)
    },
    lastPage () {
      this.separator = this.count - 4
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./separator.scss";
</style>
