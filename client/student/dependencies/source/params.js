const Config = {
  SITE_ROUTER: `{
    alias: true,
    component: true,
    redirect: false
  }`,
  SITE_SOURCE: `{
    vue: true,
    scss: true,
    js: false
  }`,
  SITE_EXAMPLE: false
}

const Remove = {
  SITE_COMPONENTS: `,
  components: SITE_COMPONENTS`,
  SITE_ROUTER: `,
  router: SITE_ROUTER`,
  SITE_EXAMPLE: `,
  example: SITE_EXAMPLE`
}

const Scss = {
  template: `// include module
@import 'SITE_SCSS_FLEX';
@import 'SITE_SCSS_UNIT';
// current sass
.SITE_SCSS_NAME {}`,
  SITE_SCSS_NAME: `
.SITE_SCSS_NAME {}`
}

const Vue = {
  SITE_CHUNK: `,
    SITE_CHUNK`,
  SITE_CHUNK_CONTENT: `
    SITE_CHUNK`,
  SITE_DEPENDENCE: `
SITE_DEPENDENCE`,
  SITE_MODULES_FIELD: `import SITE_MODULE_NAME from 'SITE_MODULE_DIR/SITE_MODULE_FILE'
SITE_MODULES_FIELD`,
  SITE_COMPONENT_FIELD: `import SITE_COMPONENT_NAME from 'SITE_COMPONENT_DIR/SITE_COMPONENT_FILE/SITE_COMPONENT_FILE.vue'
SITE_COMPONENT_FIELD`,
  SITE_CHUNK_FIELD: `SITE_CHUNK_NAME,
    SITE_CHUNK_FIELD`,
  SITE_DATE_FIELD: `SITE_DATE_KEY: SITE_DATE_VALUE,
      SITE_DATE_FIELD`,
  SITE_DATE_TATIL: `
      SITE_DATE_FIELD`,
  SITE_MODULES_NONE_FIELD: `
SITE_MODULES_FIELD `,
  SITE_COMPONENT_NONE_FIELD: `
SITE_COMPONENT_FIELD`,
  SITE_CHUNK_NONE_FIELD: `,
    SITE_CHUNK_FIELD`,
  SITE_CHUNK_TATIL: `
SITE_CHUNK_FIELD`,
  SITE_EMPTY_CHUNK: `,
  components: {
    // include chunk
  }`,
  SITE_EMPTY_DEPENDENCE: `
// include dependence
export default {`,
  SITE_EMPTY_DATA: `// start datas
      // end datas`,
  SITE_DATE_NONE_FIELD: `,
      SITE_DATE_FIELD`,
  SITE_START_NOTE: `<!-- s SITE_NOTE -->`,
  SITE_END_NOTE: `<!-- s SITE_NOTE -->`,
  SITE_REFRESH_DATA: `// start datas
      SITE_DATE
      // end datas`,
  SITE_REFRESH_DEPENDENCE: `
// include dependence
SITE_DEPENDENCE
export default {`,
  SITE_REFRESH_CHUNK: `,
  components: {
    SITE_CHUNK
    // include chunk
  }`
}

const Router = {
  SITE_COMPONENT_FIELD: `const SITE_COMPONENT_NAME = () => import(/* webpackChunkName: 'SITE_NAME' */ 'SITE_COMPONENT_PATH')
SITE_COMPONENT_FIELD`
}

const Objects = {
  SITE_JSON: `{
SITE_CONTENT_JSON,
SITE_JSON}`,
  SITE_JSON_TATIL: `,
SITE_CONTENT_JSON,
SITE_JSON`,
  SITE_JSON_KEY_VALUE: `KEY: VALUE`,
  SITE_JSON_CONTENT: `SITE_CONTENT_JSON,
SITE_JSON`,
  SITE_JSON_SAPCE: `
SITE_SPACE`,
  SITE_ARRAY: `[
SITE_CONTENT_ARRAY,
SITE_ARRAY]`,
  SITE_ARRAY_CONTENT: `SITE_CONTENT_ARRAY,
SITE_ARRAY`,
  SITE_ARRAY_TATIL: `,
SITE_CONTENT_ARRAY,
SITE_ARRAY`,
  SITE_ARRAY_SAPCE: `
SITE_SPACE`,
}

module.exports = {
  Config,
  Remove,
  Scss,
  Vue,
  Router,
  Objects
}
