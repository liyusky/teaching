const fs = require('fs')
const path = require('path')

const Tools_path = path.join(__dirname, './tools.js')
const Source_path = path.join(__dirname, './source.js')
const Params_Path = path.join(__dirname, '../source/params.js')
const Sources_path = path.join(__dirname, '../source/sources.js')
const Address_path = path.join(__dirname, '../source/address.js')

const Tools = require(Tools_path)
const Source = require(Source_path)
const Sources = require(Sources_path)
const Address = require(Address_path)
const {Vue} = require(Params_Path)

class Template {
  static get innerConfig () {
    let {modules} = Sources
    let model = ''
    modules.forEach(item => {
      model += `\n\t\t'${Tools.firstChatUp(item.split('.')[0])}': false,`
    })
    return Tools.setInnerConfigTempalte({
      modules: model
    })
  }

  static get outerConfig () {
    let {components, modules} = Sources
    let [component, model] = ['', '']
    components.forEach(item => {
      if (!item.includes('.')) component += `\n\t\t'${item}': false,`
    })
    modules.forEach(item => {
      model += `\n\t\t'${Tools.firstChatUp(item.split('.')[0])}': false,`
    })
    return Tools.setOuterConfigTempalte({
      modules: model,
      components: component
    })
  }

  static refreshConfig (params) {
    let {config, type} = params
    return (type ? Template.refreshOuterConfig(config) : Template.refreshInnerConfig(config))
  }

  static refreshOuterConfig (config) {
    let {note, source, modules, components, router} = config
    let [sources, model, component, routers] = ['', '', '', '']
    for (let [key, value] of Object.entries(source)) {
      sources += `\n\t\t'${key}': ${value},`
    }

    for (let [key, value] of Object.entries(modules)) {
      key = key.includes('-') ? `'${key}'` : key
      model += `\n\t\t${key}: ${value},`
    }

    for (let [key, value] of Object.entries(components)) {
      value = (typeof value === 'object') ? Tools.objectTransformString(value, 2) : value
      key = key.includes('-') ? `'${key}'` : key
      component += `\n\t\t${key}: ${value},`
    }

    for (let [key, value] of Object.entries(router)) {
      value = (typeof value === 'object') ? JSON.stringify(value) : value
      key = key.includes('-') ? `'${key}'` : key
      routers += `\n\t\t${key}: ${value},`
    }

    return Tools.refreshOuterConfigTempalte({
      note,
      source: sources,
      modules: model,
      components: component,
      router: routers
    })
  }

  static refreshInnerConfig (config) {
    let {note, source, modules, example} = config
    let [sources, model] = ['', '', '', '']
    for (let [key, value] of Object.entries(source)) {
      sources += `\n\t\t${key}: ${value},`
    }
    for (let [key, value] of Object.entries(modules)) {
      model += `\n\t\t${key}: ${value},`
    }

    example = Tools.objectTransformString(example, 1)

    return Tools.refreshInnerConfigTempalte({
      note,
      source: sources,
      modules: model,
      example
    })
  }

  static scss (params) {
    let {refresh, address, template} = params
    template = Tools.setScssTemplate(params)
    if (refresh) {
      let content = fs.readFileSync(address, 'utf8')
      template = content.replace(/\/\/ include module[^]*\/\/ current sass/, template)
    }
    return template
  }

  static js (params) {
    return ''
  }

  static vue (params) {
    let {config: {modules, components, note}, name, address, refresh, template} = params
    let modulesDict = Source.modules
    let [model, component, chunk, data, dependence] = [
      'SITE_MODULES_FIELD',
      'SITE_COMPONENT_FIELD',
      'SITE_CHUNK_FIELD',
      'SITE_DATE_FIELD',
      ''
    ]
    let paths = {
      modules: path.relative(address, Address.modules).replace(/\\/g, '/').replace('../', ''),
      components: path.relative(address, Address.components).replace(/\\/g, '/').replace('../', '')
    }
    for (let [key, value] of Object.entries(modules)) {
      if (value) {
        model = model.replace('SITE_MODULES_FIELD', Vue.SITE_MODULES_FIELD)
        model = model.replace('SITE_MODULE_NAME', key)
        model = model.replace('SITE_MODULE_DIR', paths.modules)
        model = model.replace('SITE_MODULE_FILE', modulesDict[key])
      }
    }

    if (components) {
      for (let [key, value] of Object.entries(components)) {
        if (value || value === null) {
          component = component.replace('SITE_COMPONENT_FIELD', Vue.SITE_COMPONENT_FIELD)
          component = component.replace('SITE_COMPONENT_NAME', Tools.setComponentsName(key))
          component = component.replace('SITE_COMPONENT_DIR', paths.components)
          component = component.replace(/SITE_COMPONENT_FILE/g, key)

          chunk = chunk.replace('SITE_CHUNK_FIELD', Vue.SITE_CHUNK_FIELD)
          chunk = chunk.replace('SITE_CHUNK_NAME', Tools.setComponentsName(key))

          if (value !== null) {
            data = data.replace('SITE_DATE_FIELD', Vue.SITE_DATE_FIELD)
            data = data.replace('SITE_DATE_KEY', key.includes('-') ? Tools.setParamsName(key) : key)
            data = data.replace('SITE_DATE_VALUE', Tools.objectTransformString(value, 3))
          }
        }
      }
      component = component.replace(Vue.SITE_COMPONENT_NONE_FIELD, '')
      chunk = chunk.replace(Vue.SITE_CHUNK_NONE_FIELD, '')
      chunk = chunk.replace('SITE_CHUNK_FIELD', '')
      data = data.replace(Vue.SITE_DATE_NONE_FIELD, '')
      data = data.replace('SITE_DATE_FIELD', '')
    }
    else {
      component = ''
      chunk = ''
      data = ''
    }

    dependence = model.replace('SITE_MODULES_FIELD', component)
    dependence = dependence.replace('SITE_COMPONENT_FIELD', '')

    if (refresh) {
      template = fs.readFileSync(address, 'utf8')
      template = Tools.refreshVueTemplate({note, data, dependence, chunk, template})
    }
    else {
      template = Tools.initVueTemplate({name, note, data, dependence, chunk})
    }

    return template
  }
}

module.exports = Template