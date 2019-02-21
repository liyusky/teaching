<template>
  <!-- s  -->
  <section class="code">
    <div class="code-record">
      <div class="record-table" v-show="showRecord">
        <table class="table-header table-reset">
          <tr>
            <th class="table-100">序号</th>
            <th class="table-100">结果</th>
            <th class="table-100">成绩</th>
            <th class="table-130">提交时间</th>
            <th class="table-100">代码</th>
          </tr>
        </table>
        <div class="table-content">
          <table class="table-reset">
            <tr v-for="(item, index) in table" :key="index">
              <td class="table-100">{{index + 1}}</td>
              <td class="table-100">{{item.success ? '成功' : '失败'}}</td>
              <td class="table-100">{{item.score}}</td>
              <td class="table-130">{{TimeModule.format('YYYY-MM-DD HH-mm-ss', item.time)}}</td>
              <td class="table-100">
                <button class="content-show-detail" @click="showCode(item, index)">查看</button>
              </td>
            </tr>
          </table>
        </div>
      </div>
      <div class="record-roll-back" @click="rollback">↓</div>
    </div>
    <div class="record-code" v-show="showCodeContent">
      <div class="code-title">
        <p>章节：{{chapter}}，关卡：{{stage}}，提交：第{{submit + 1}}次</p>
        <p>分数：{{score}}</p>
      </div>
      <pre>
        <code class="cpp hljs" id="code"></code>
      </pre>
    </div>
    <div class="record-result" v-show="showCodeContent">
      <p class="result-title">运行结果：</p>
      <p class="result-content">{{result}}</p>
    </div>
    <div class="record-output" v-show="showCodeContent">
      <p class="output-title">输出：</p>
      <p class="output-content">{{output}}</p>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../../../dependencies/modules/Communication.class.js'
import Http from '../../../../../../dependencies/modules/Http.class.js'
import Time from '../../../../../../dependencies/modules/Time.class.js'

export default {
  name: 'CodeDetailComponent',
  data () {
    return {
      showCodeContent: false,
      showRecord: true,
      TimeModule: Time,
      result: '',
      output: '',
      score: 0,
      table: [],
      chapter: Communication.detail.chapter,
      submit: -1,
      stage: Communication.detail.stage
    }
  },
  created () {
    this.getGameStageRecode()
  },
  methods: {
    rollback () {
      this.showRecord = !this.showRecord
    },
    getGameStageRecode () {
      Http.send({
        url: 'GameStageRecord',
        data: {
          gsid: Communication.detail.gsid,
          student: Communication.detail.student
        }
      }).success(data => {
        this.table = data
      }).fail(data => {
      }).default(() => {
      })
    },
    showCode (item, index) {
      this.submit = index
      this.showCodeContent = true
      Http.send({
        url: 'SourceCode',
        data: {
          mrcid: item.mrcid
        }
      }).success(data => {
        this.result = data.result || ''
        this.output = data.output || ''
        this.score = data.score
        this.success = data.success
        let codeDom = document.getElementById('code')
        let $ = window.$
        $('code').text(data.code || '')
        window.hljs.configure({
          languages: 'cpp'
        })
        window.hljs.highlightBlock(codeDom)
        $.each($('code'), (index, item) => {
          $(item).html(`<ul class="content"><li>${$(item).html().replace(/\n/g, '\n</li><li>')}\n</li></ul>`)
        })
      }).fail(data => {
        console.log(data)
      })
    }
  }
}
</script>

<style lang="sass" scoped>
@import "./code.scss";
</style>
