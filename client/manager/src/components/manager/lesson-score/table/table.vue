<template>
  <!-- s  -->
  <section class="table">
    <table class="table-header table-reset">
      <tr>
        <th class="table-70">操作</th>
        <th class="table-70">序号</th>
        <th class="table-70">姓名</th>
        <th class="table-100" v-for="(item, index) in range" :key="index">
          <p>{{stage[current + index]}}</p>
          <div class="arrow-left" v-if="index == 0" @click="leftMove"></div>
          <div class="arrow-right" v-if="index == (range -1)" @click="rightMove"></div>
        </th>
      </tr>
    </table>
    <div class="table-content">
      <table class="table-reset">
        <tr v-for="(item, index) in table" :key="index">
          <td class="table-70">
            <button class="content-show-detail" @click="openDetail(item)">详情</button>
          </td>
          <td class="table-70">{{index + 1}}</td>
          <td class="table-70">{{item.name}}</td>
          <td class="table-100" v-for="rindex in range" :key="rindex">
            <button class="content-btn" :disabled="getDisable(item.score[current + rindex - 1])" :class="getColor(item.score[current + rindex - 1])" @click="showCode(rindex, item)">{{item.score[current + rindex - 1]}}</button>
          </td>
        </tr>
      </table>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../dependencies/modules/Communication.class.js'
import Display from '../../../../../dependencies/modules/Display.class.js'
import Http from '../../../../../dependencies/modules/Http.class.js'

export default {
  name: 'TableComponent',
  props: ['oid', 'cid', 'lid', 'organization', 'course', 'lesson'],
  data () {
    return {
      range: 4,
      table: [],
      stage: [],
      stages: [],
      current: 0,
      gsids: [],
      games: [],
      max: 0
      // DictionaryModule: Dictionary
      // start datas
      // end datas
    }
  },
  methods: {
    getDisable (score) {
      console.log(score)
      if (score || score === 0) {
        return false
      } else {
        return true
      }
    },
    getColor (score) {
      if (score) {
        score = score * 1
        let state = ''
        if (score * 1 === 100) {
          state = 'success'
        } else if (score > 0 && score < 100) {
          state = 'warning'
        } else if (score === 0) {
          state = 'fail'
        }
        return `btn-${state}`
      }
    },
    getScoreList (gcid, oid, question) {
      this.clearParams()
      if (gcid <= 0) return
      if (oid <= 0) return
      Http.send({
        url: 'ExampleScoreList',
        data: {
          oid: oid,
          gcid: gcid
        }
      }).success(data => {
        this.table = this.formatData(data, question)
      }).fail(data => {
      }).default(() => {
        Display.api = false
      })
    },
    formatData (data, example) {
      let map = {}
      let table = []
      let lid = example.lesson
      let students = {}
      let stages = {}

      this.max = data.stage.length > this.max ? data.stage.length : this.max
      this.range = this.max > 4 ? 4 : this.max

      let stageArray = []
      let stagesArr = []
      data.stage.forEach(item => {
        stageArray.push(item.name)
        stagesArr.push(item.gsid)
      })
      this.gsids = stagesArr
      this.stage = stageArray

      data.score.forEach(sitem => {
        if (!(sitem.sid in students)) students[sitem.sid] = {}
        if (!(sitem.stage.id in stages)) stages[sitem.stage.id] = sitem.stage.name
        students[sitem.sid][sitem.stage.id] = sitem.high_score
      })

      for (let sid in students) {
        let stages = students[sid]
        map[sid] = []
        data.stage.forEach(item => {
          map[sid][item.gsid] = stages[item.gsid]
        })
      }

      data.student.forEach(item => {
        let source = {
          ...item.studentDetail,
          student: item.student,
          lid: lid
        }

        let scoreArr = map[item.student] || []
        let resultArr = []
        scoreArr.forEach((item, index) => {
          resultArr.push(item)
        })
        source.score = resultArr

        table.push(source)
      })
      return table
    },
    rightMove () {
      if (this.max > 4 && this.current + this.range < this.max) this.current += 1
    },
    leftMove () {
      if (this.current > 0) this.current -= 1
    },
    openDetail (item) {
      item = {
        ...item,
        organization: this.organization,
        course: this.course,
        lesson: this.lesson,
        component: 'summary',
        gsid: this.gsids,
        stage: this.stage,
        games: this.games
      }
      Communication.detail = item
      Display.detail = 'lesson-code'
    },
    showCode (index, item) {
      Display.detail = 'code'
      item = {
        ...item,
        organization: this.organization,
        course: this.course,
        lesson: this.lesson,
        gsid: this.gsids[this.current + index - 1],
        component: 'code'
      }
      Communication.detail = item
    },
    clearParams () {
      this.range = 4
      this.table = []
      this.stage = []
      this.stages = []
      this.current = []
      this.current = 0
      this.gsids = 0
      this.games = []
      this.max = []
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./table.scss";
</style>
