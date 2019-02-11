module.exports = {
  note: '成绩管理',
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
    Http: true,
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
    'search-bar': false,
    separator: null,
    template: false
  }
}