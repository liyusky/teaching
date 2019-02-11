<template>
  <!-- s  -->
  <section class="lesson-score">
    <div class="score-nav">
      <div class="nav-select">
        <div class="select-item fl" @click="selectClass">{{organization}}</div>
        <div class="select-item fl" @click="selectCourse">{{course}}</div>
        <div class="select-item fl" @click="selectLesson">{{lesson}}</div>
      </div>
    </div>
    <div class="score-chapters">
      <div class="chapters-item fl" v-for="(item, index) in chapters" :key="index" @click="queryStage(item, index)" :class="{'selected': current == index}">{{item.detail.chapter}}</div>
    </div>
    <TableComponent :oid="oid" :cid="cid" :lid="lid" :organization="organization" :course="course" :lesson="lesson" :gcid="gcid" ref="table"></TableComponent>
    <!-- <SeparatorComponent></SeparatorComponent> -->
  </section>
  <!-- s  -->
</template>

<script>
import TableComponent from './table/table.vue'
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Dictionary from '../../../../dependencies/modules/Dictionary.class.js'
import Display from '../../../../dependencies/modules/Display.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'

export default {
  name: 'LessonScoreComponent',
  data () {
    return {
      chapters: [],
      oid: 0,
      cid: 0,
      lid: 0,
      gcid: 0,
      organization: '选择班级',
      course: '选择课程',
      lesson: '选择课时'
      // start datas
      // end datas
    }
  },
  components: {
    // include chunk
    TableComponent
  },
  mounted () {
    Account.logout()
  },
  methods: {
    selectLesson () {
      if (this.cid <= 0) {
        alert('请选择课程')
        return
      }
      Communication.modal = this.cid
      Display.modal = 'lesson-select'
    },
    selectCourse () {
      if (this.oid <= 0) {
        alert('请选择班级')
        return
      }
      Display.modal = 'course-select'
    },
    selectClass () {
      Display.modal = 'class-select'
    },
    getChapters () {
      if (this.oid === 0) return
      if (this.cid === 0) return
      if (this.lid === 0) return
      Http.send({
        url: 'ExampleList',
        data: {
          lid: this.lid,
          enable: 2
        }
      }).success(data => {
        this.chapters = data
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    queryStage (item, index) {
      this.current = index
      this.gcid = item.gcid
      this.$refs.table.getScoreList(this.gcid, this.oid, item)
    }
  },
  watch: {
    '$store.state.modal' (modal, previous) {
      console.log(Communication.modal)
      if (previous === 'course-select' && modal === false && Communication.modal) {
        this.course = `${Communication.modal.name}（${Dictionary.language[Communication.modal.language]}，${Dictionary.rank[Communication.modal.grade]}）`
        this.cid = {...Communication.modal}.cid
        Communication.modal = false
      } else if (previous === 'class-select' && modal === false && Communication.modal) {
        this.organization = `${Communication.modal.name}（${Communication.modal.manager.name} ${Communication.modal.manager.phone}）`
        this.oid = {...Communication.modal}.oid
        Communication.modal = false
      } else if (previous === 'lesson-select' && modal === false && Communication.modal && 'lid' in Communication.modal) {
        this.lesson = Communication.modal.name
        this.lid = {...Communication.modal}.lid
        Communication.modal = false
      }
    },
    oid () {
      this.getChapters()
    },
    cid () {
      this.getChapters()
    },
    lid () {
      this.getChapters()
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./lesson-score.scss";
</style>
