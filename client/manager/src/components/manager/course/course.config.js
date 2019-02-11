module.exports = {
  note: '课程管理',
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
    Communication: false,
    Dictionary: false,
    Display: true,
    Http: false,
    Router: false,
    Time: false,
    Url: false
  },
  components: {
    btn: {
      type: 'addition'
    },
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
