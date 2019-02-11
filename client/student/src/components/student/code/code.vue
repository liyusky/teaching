<template>
  <!-- s  -->
  <section class="commit-record">
    <div class="record-code">
      <div class="code-title">源码</div>
      <pre>
        <code class="cpp hljs" id="code"></code>
      </pre>
    </div>
    <div class="record-result">
      <div class="result-title">运行结果</div>
      <textarea class="result-content" readonly v-model="result"></textarea>
    </div>
    <div class="record-output">
      <div class="output-title">输出结果</div>
      <textarea class="output-content" readonly v-model="output"></textarea>
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
      output: ''
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
        let codeDom = document.getElementById('code')
        codeDom.innerText = data.code || ''
        window.hljs.highlightBlock(codeDom)
        let $ = window.$
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
