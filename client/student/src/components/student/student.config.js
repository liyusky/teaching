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
    redirect: '../student/course/course.vue',
    home: false
  },
  modules: {
    Account: false,
    Check: false,
    Communication: false,
    Dictionary: false,
    Display: false,
    Http: false,
    Router: false,
    Storage: false,
    Time: false,
    Url: false
  },
  components: {
    exhibition: false,
    header: null,
    'homework-panel': false,
    'image-bg': false,
    inputs: false,
    nva: null,
    schedule: false,
    title: false
  }
}
