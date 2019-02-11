module.exports = {
  note: '作业管理',
  source: {
    'vue': true,
    'scss': true,
    'js': false
  },
  router: {
    alias: true,
    component: true,
    redirect: false,
    home: false
  },
  modules: {
    Account: true,
    Check: false,
    Communication: true,
    Dictionary: true,
    Display: true,
    Http: false,
    Router: false,
    Time: false,
    Url: false
  },
  components: {
    btn: false,
    'detail-panel': false,
    'image-bg': false,
    inputs: false,
    modal: false,
    panel: false,
    'search-bar': null,
    separator: null,
    template: false
  }
}
