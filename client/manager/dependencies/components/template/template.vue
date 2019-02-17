<template>
  <!-- s 页面模板 -->
  <section class="template">
    <div class="template-menu">
      <div class="menu-logo">
        <img class="logo-image" src="../../../static/images/title-logo.png">
      </div>
      <ul class="menu-list">
        <li class="list-item" v-for="(item, index) in menu" :class="{'selected': item.page == current}" :key="index" @click="showContent(item.page)">
          <i class="item-icon"></i>
          <span class="item-name">{{item.name}}</span>
        </li>
      </ul>
    </div>
    <div class="template-content">
      <div class="content-title">
        <div class="title-tip" @click="showNav">
          <span>{{account.name || '未实名'}}</span>
          <i class="iconfont icon-arrow-down color-light-black"></i>
        </div>
        <ul class="title-option-list" v-show="nav">
          <li class="list-item" @click="updateAccount">
            <i class=""></i>
            <span class="item-name">修改个人信息</span>
          </li>
          <li class="list-item" @click="quit">
            <i class=""></i>
            <span class="item-name">退出</span>
          </li>
        </ul>
      </div>
      <slot></slot>
    </div>
  </section>
  <!-- s 页面模板 -->
</template>

<script>
// include dependence
import Http from '../../modules/Http.class.js'
import Account from '../../modules/Account.class.js'
import Display from '../../modules/Display.class.js'
import Router from '../../modules/Router.class.js'

export default {
  name: 'TemplateComponent',
  data () {
    return {
      current: 'manager-class',
      menu: [
        {
          name: '班级管理',
          icon: '',
          page: 'manager-class'
        },
        {
          name: '课程管理',
          icon: '',
          page: 'manager-course'
        },
        {
          name: '课程表管理',
          icon: '',
          page: 'manager-curriculum'
        },
        {
          name: '作业管理',
          icon: '',
          page: 'manager-homework'
        },
        {
          name: '作业成绩管理',
          icon: '',
          page: 'manager-score'
        },
        {
          name: '课时内容成绩管理',
          icon: '',
          page: 'manager-lesson-score'
        }
      ],
      nav: false,
      account: Account
    }
  },
  components: {
    // include chunk
  },
  created () {
    if (Router.menu) this.current = Router.menu
    if (Account.role >= 99) {
      this.menu.push({
        name: '学员管理',
        icon: '',
        page: 'manager-student'
      })
      this.menu.push({
        name: '教师管理',
        icon: '',
        page: 'manager-teacher'
      })
    }
  },
  methods: {
    showContent (page) {
      this.current = page
      Router.menu = page
      Router.push(page)
    },
    showNav () {
      this.nav = !this.nav
    },
    updateAccount () {
      Display.panel = 'user-update-user'
      this.nav = false
    },
    quit () {
      Http.send({
        url: 'Logout'
      }).success(data => {
        this.clearStorage()
        Router.push('login')
      }).fail(data => {
        alert('退出失败')
      }).default(() => {
      })
    },
    clearStorage () {
      this.$store.commit('account', {})
      this.$store.commit('origin', null)
      this.$store.commit('modal', false)
      this.$store.commit('panel', false)
      this.$store.commit('detail', false)
      this.$store.commit('api', false)
      this.$store.commit('tip', false)
      this.$store.commit('content', false)
      this.$store.commit('communication', {})
      this.$store.commit('menu', '')
      localStorage.clear()
    }
  },
  watch: {
    '$store.state.account' (account) {
      this.account = account
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./template.scss";
</style>
