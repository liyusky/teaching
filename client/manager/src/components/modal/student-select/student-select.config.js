module.exports = {
  note: '',
  source: {
    'vue': true,
    'scss': true,
    'js': false
  },
  router: {
    alias: true,
    component: true,
    redirect: false,
    home: undefined
  },
  modules: {
    Account: false,
    Check: false,
    Communication: true,
    Dictionary: false,
    Display: true,
    Http: true,
    Router: false,
    Time: false,
    Url: false
  },
  components: {
    btn: {
      type: 'operation'
    },
    'detail-panel': false,
    'image-bg': false,
    inputs: false,
    modal: false,
    panel: false,
    'search-bar': null,
    separator: false,
    template: false
  }
}
