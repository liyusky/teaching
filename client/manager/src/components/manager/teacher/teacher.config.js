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
    home: false
  },
  modules: {
    Account: false,
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
