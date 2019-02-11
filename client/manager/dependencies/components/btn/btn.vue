<template>
  <!-- s 按钮组件 -->
  <section class="btn" :class="setting.type">
    <button class="addition" v-if="setting.type == 'addition'" @click="clickThisBtn">
      <slot></slot>
    </button>
    <button class="confirm" v-if="setting.type == 'operation'">确认</button>
    <button class="cancel" v-if="setting.type == 'operation'">取消</button>
  </section>
  <!-- s 按钮组件 -->
</template>

<script>
// include dependence
export default {
  name: 'BtnComponent',
  props: ['setting'],
  data () {
    return {
    }
  },
  components: {
    // include chunk
  },
  methods: {
    clickThisBtn () {
      this.$emit('BTN_CLICK_EVENT')
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./btn.scss";
</style>
