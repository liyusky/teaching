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
    home: true
  },
  modules: {
    Account: true,
    Check: true,
    Communication: false,
    Dictionary: false,
    Display: true,
    Http: true,
    Router: true,
    Storage: false,
    Time: false,
    Url: false
  },
  components: {
    exhibition: false,
    header: false,
    'homework-panel': false,
    'image-bg': '../../../static/images/bg.jpg',
    inputs: null,
    nva: false,
    schedule: false,
    title: false
  }
}
