<template>
  <!-- s  -->
  <section class="course">
    <div class="course-list" v-for="(section, index) in menu" :key="index">
      <div class="list-title">
        <div>{{section.title}}</div>
      </div>
      <ExhibitionComponent v-for="(item, index) in section.exhibition" :key="index" :exhibition="item">
        <div class="list-exhibition">
          <p v-if="item.name">{{item.name}}</p>
          <p class="exhibition-tecdate" v-if="item.teacher">{{item.teacher}}</p>
          <p class="exhibition-date" v-if="item.date">{{item.date}}</p>
        </div>
      </ExhibitionComponent>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Account from '../../../../dependencies/modules/Account.class.js'
import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'
import ExhibitionComponent from '../../../../dependencies/components/exhibition/exhibition.vue'
import TitleComponent from '../../../../dependencies/components/title/title.vue'
export default {
  name: 'CourseComponent',
  data () {
    return {
      title: '首页',
      menu: []
    }
  },
  components: {
    ExhibitionComponent,
    TitleComponent
    // include component
  },
  created () {
    Account.logout()
    this.getCourseList()
  },
  methods: {
    getCourseList () {
      Http.send({
        url: 'CourseList'
      }).success(data => {
        this.menu = this.formatStudentData(data)
      }).fail(() => {
      })
    },
    formatStudentData (data) {
      let menu = []
      let map = {}
      data.forEach(item => {
        if (!(item.oid in map)) {
          let name = item.name
          // let manager = `${item.manager.name}(${organization.manager.phone})`
          let time = `${item.launch.split('T')[0]}~${item.deadline.split('T')[0]}`
          // let school = `${organization.school.name}${organization.school.district}${Dictionary.rank[organization.school.level]}`
          map[item.oid] = {
            title: `${name}[${time}](${this.setFinishStatus(item.launch, item.deadline)})`,
            exhibition: []
          }
        }
        let exhibition = []
        item.detail.course.forEach(course => {
          exhibition.push({
            tid: course.teacher.tid,
            tpid: course.teacher.tpid,
            teacher: course.teacher.name,
            cid: course.course.id,
            oid: item.oid,
            sid: Account.uid,
            student: Account.name,
            launch: course.launch,
            deadline: course.deadline,
            title: `${course.course.name}(${Dictionary.language[course.course.language]})`,
            date: `${course.launch.split('T')[0]}-${course.deadline.split('T')[0]}`,
            page: 'student-lesson',
            btn: '查看详情'
          })
        })
        map[item.oid].exhibition = exhibition
      })
      for (let key in map) {
        menu.push(map[key])
      }
      console.log(menu)
      return menu
    },
    setFinishStatus (launch, deadline) {
      launch = (new Date(launch)).getTime()
      deadline = (new Date(deadline)).getTime()
      let now = (new Date()).getTime()
      if (now < launch) {
        return '未开始'
      } else if (now > deadline) {
        return '已结束'
      } else {
        return '进行中'
      }
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./course.scss";
</style>
