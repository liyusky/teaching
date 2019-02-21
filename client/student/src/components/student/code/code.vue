<template>
  <!-- s  -->
  <section class="commit-record">
    <div class="record-code">
      <div class="code-title">
        <p>章节：{{origin.chapter}}，关卡：{{origin.stage}}，提交：第{{origin.submit + 1}}次</p>
        <p>分数：{{score}}</p>
      </div>
      <pre>
        <code class="cpp hljs" id="code">
        </code>
      </pre>
    </div>
    <div class="record-result">
      <p class="result-title">运行结果：</p>
      <p class="result-content">{{result}}</p>
    </div>
    <div class="record-output">
      <p class="output-title">输出：</p>
      <p class="output-content">{{output}}</p>
    </div>
  </section>
  <!-- s  -->
</template>

<script>
// include dependence
import Communication from '../../../../dependencies/modules/Communication.class.js'
import Http from '../../../../dependencies/modules/Http.class.js'
import Account from '../../../../dependencies/modules/Account.class.js'

export default {
  name: 'CommitRecordComponent',
  data () {
    return {
      code: '',
      result: '',
      output: '',
      origin: Communication.code,
      score: 0,
      success: 0
      // start params
      // end params
    }
  },
  components: {
    // include components
  },
  created () {
    Account.logout()
    this.getCode()
  },
  methods: {
    getCode () {
      Http.send({
        url: 'SourceCode',
        data: {
          mrcid: Communication.code.mrcid
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
