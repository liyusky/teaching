const fs = require('fs')
const path = require('path')

const Params_Path = path.join(__dirname, '../source/params.js')
const {Remove, Config, Vue, Scss, Objects} = require(Params_Path)
const Address_path = path.join(__dirname, '../source/address.js')
const Template_path = path.join(__dirname, '../source/template.js')

const Templates = require(Template_path)
const Address = require(Address_path)

class Tool {
  static firstChatUp (word) {
    return word.substring(0, 1).toUpperCase() + word.substring(1)
  }

  static setParamsName (name) {
    let nameArr = name.split('-')
    nameArr.forEach((value, index) => {
      if (index) {
        nameArr[index] = value.substring(0, 1).toUpperCase() + value.substring(1)
      }
    })
    return nameArr.join('')
  }

  static getContentResolvePath (dir, name, type) {
    let types = {
      vue: 'vue',
      config: 'config.js',
      js: 'js',
      sass: 'scss'
    }
    return './' + path.join(dir, `${name}.${types[type]}`).replace('\\', '\/')
  }

  static refreshConfigTempalte (params) {
    let {router, modules, components, note, example, source, template} = params
    modules = modules ? `{${modules.substr(0, modules.length - 1) + '\n\t'}}` : false
    components = components ? `{${components.substr(0, components.length - 1) + '\n\t'}}` : false
    template = Templates.config.replace('SITE_EXAMPLE', example)
    template = template.replace('SITE_NOTE', note)
    template = template.replace('SITE_MODULES', modules)
    template = template.replace('SITE_COMPONENTS', components)
    template = template.replace('SITE_ROUTER', router)
    template = template.replace('SITE_SOURCE', source)
    template = template.replace(/\t/g, '  ')
    return template
  }

  static setInnerConfigTempalte (params) {
    let {modules, template} = params
    modules = modules ? `{${modules.substr(0, modules.length - 1) + '\n\t'}}` : false
    template = Templates.config.replace(Remove.SITE_COMPONENTS, '')
    template = template.replace(Remove.SITE_ROUTER, '')
    template = template.replace('SITE_EXAMPLE', false)
    template = template.replace('SITE_NOTE', '')
    template = template.replace('SITE_MODULES', modules)
    template = template.replace('SITE_SOURCE', Config.SITE_SOURCE)
    template = template.replace(/\t/g, '  ')
    return template
  }

  static setOuterConfigTempalte (params) {
    let {modules, components, template} = params
    modules = modules ? `{${modules.substr(0, modules.length - 1) + '\n\t'}}` : false
    components = components ? `{${components.substr(0, components.length - 1) + '\n\t'}}` : false
    template = Templates.config.replace(Remove.SITE_EXAMPLE, '')
    template = template.replace('SITE_NOTE', '')
    template = template.replace('SITE_MODULES', modules)
    template = template.replace('SITE_COMPONENTS', components)
    template = template.replace('SITE_ROUTER', Config.SITE_ROUTER)
    template = template.replace('SITE_SOURCE', Config.SITE_SOURCE)
    template = template.replace(/\t/g, '  ')
    return template
  }

  static refreshOuterConfigTempalte (params) {
    let {note, source, router, modules, components, template} = params
    modules = `{${modules.substr(0, modules.length - 1) + '\n\t'}}`
    components = `{${components.substr(0, components.length - 1) + '\n\t'}}`
    source = `{${source.substr(0, source.length - 1) + '\n\t'}}`
    router = `{${router.substr(0, router.length - 1) + '\n\t'}}`
    template = Templates.config.replace(Remove.SITE_EXAMPLE, '')
    template = template.replace('SITE_NOTE', note)
    template = template.replace('SITE_MODULES', modules)
    template = template.replace('SITE_COMPONENTS', components)
    template = template.replace('SITE_ROUTER', router)
    template = template.replace('SITE_SOURCE', source)
    template = template.replace(/\t/g, '  ')
    return template
  }

  static refreshInnerConfigTempalte (params) {
    let {note, source, modules, example, template} = params
    modules = `{${modules.substr(0, modules.length - 1) + '\n\t'}}`
    source = `{${source.substr(0, source.length - 1) + '\n\t'}}`
    template = Templates.config.replace(Remove.SITE_COMPONENTS, '')
    template = template.replace(Remove.SITE_ROUTER, '')
    template = template.replace('SITE_NOTE', note)
    template = template.replace('SITE_MODULES', modules)
    template = template.replace('SITE_EXAMPLE', example)
    template = template.replace('SITE_SOURCE', source)
    template = template.replace(/\t/g, '  ')
    return template
  }


  static createFile (path, content, refresh) {
    let result = fs.writeFileSync(path, content)
    let state = '创建'
    if (refresh) state = '更新'
    let logStr = `${path} ${state}成功`
    if (result) {
      logStr = `${path} ${state}失败 ===== ${result}`
    }
  }

  static setComponentsName (name) {
    let nameArr = name.split('-')
    nameArr.forEach((value, index) => {
      nameArr[index] = value.substring(0, 1).toUpperCase() + value.substring(1)
    })
    nameArr.push('Component')
    return nameArr.join('')
  }

  static setScssTemplate (params) {
    let {address, name, refresh, template} = {...params, ...Scss}
    template = template.replace('SITE_SCSS_FLEX', path.relative(address, Address.flex).replace(/\\/g, '/').replace('../', ''))
    template = template.replace('SITE_SCSS_UNIT', path.relative(address, Address.unit).replace(/\\/g, '/').replace('../', ''))
    template = refresh ? template.replace(Scss.SITE_SCSS_NAME, '') : template.replace('SITE_SCSS_NAME', name)
    return template
  }

  static initVueTemplate(params) {
    let {name, note, data, dependence, chunk, template} = params
    template = Templates.vue.replace('SITE_CLASS', name)
    template = template.replace('SITE_NOTE', note)
    template = template.replace('SITE_NOTE', note)
    template = template.replace('SITE_NAME', Tool.setComponentsName(name))
    template = template.replace('SITE_DATE', data)
    template = dependence ? template.replace('SITE_DEPENDENCE', dependence): template.replace(Vue.SITE_DEPENDENCE, '')
    template = chunk ? template.replace(Vue.SITE_CHUNK, Vue.SITE_CHUNK_CONTENT.replace('SITE_CHUNK', chunk)) : template.replace(Vue.SITE_CHUNK, '')
    template = template.replace('SITE_SASS', `./${name}.scss`)
    template = template.replace(Vue.SITE_DATE_TATIL, '')
    template = template.replace(Vue.SITE_CHUNK_TATIL, '')
    return template
  }

  static refreshVueTemplate(params) {
    let {note, data, dependence, chunk, template} = params

    template = template.replace(/<!-- s [^\t\v\n\r\f]* -->/, Vue.SITE_START_NOTE.replace('SITE_NOTE', note))
    template = template.replace(/<!-- e [^\t\v\n\r\f]* -->/, Vue.SITE_END_NOTE.replace('SITE_NOTE', note))
    if (data) {
      template = template.replace(/\/\/ start datas[^]*\/\/ end datas/, Vue.SITE_REFRESH_DATA.replace('SITE_DATE', data))
    } else {
      template = template.replace(/\/\/ start datas[^]*\/\/ end datas/, Vue.SITE_EMPTY_DATA)
    }

    if (dependence) {
      template = template.replace(/\n\/\/ include dependence[^]*export default {/, Vue.SITE_REFRESH_DEPENDENCE.replace('SITE_DEPENDENCE', dependence))
    } else {
      template = template.replace(/\n\/\/ include dependence[^]*export default {/, Vue.SITE_EMPTY_DEPENDENCE)
    }

    if (chunk) {
      template = template.replace(/,\n  components: {[^]*\/\/ include chunk\n  }/, Vue.SITE_REFRESH_CHUNK.replace('SITE_CHUNK', chunk))
    } else {
      template = template.replace(/,\n  components: {[^]*\/\/ include chunk\n  }/, Vue.SITE_EMPTY_CHUNK)
    }

    return template
  }

  static getRelativePath (dir) {
    let router = path.join(__dirname, '../../src/router/router.js')
    return path.relative(router, dir).replace(/..\\/, '')
  }

  static loop (callback, params) {
    let {sources, dir, type} = params
    sources.forEach(item => {
      let currentDir = path.join(dir, item)
      let stats = fs.statSync(currentDir)
      if (stats.isDirectory()) {
        delete params.sources
        params.dir = currentDir
        params.name = item
        return callback(params)
      }
    })
  }

  static objectTransformString (content, index, mark) {
    let str = ''
    let space = this.setSpace(index)
    if (typeof content === 'object') {
      if (content instanceof Array) {
        str = Objects.SITE_ARRAY
        content.forEach(item => {
          str = str.replace('SITE_CONTENT_ARRAY', space + '  ' + this.objectTransformString(item, index + 1, mark))
          str = str.replace('SITE_ARRAY', Objects.SITE_ARRAY_CONTENT)
        })
        if (str === Objects.SITE_ARRAY) {
          str = '[]'
        } else {
          str = str.replace(Objects.SITE_ARRAY_TATIL, Objects.SITE_ARRAY_SAPCE)
          str = str.replace('SITE_SPACE', space)
        }
      }
      else if (content === null) {
        str = null
      }
      else {
        str = Objects.SITE_JSON
        for (let [key, value] of Object.entries(content)) {
          let jsonStr = Objects.SITE_JSON_KEY_VALUE
          jsonStr = jsonStr.replace('KEY', space + '  ' + key)
          if (mark && (key === 'component')) {
            let valueStr = Tool.objectTransformString(value, index + 1, mark)
            jsonStr = jsonStr.replace('VALUE', valueStr.replace(/'/g, ''))
          } else {
            jsonStr = jsonStr.replace('VALUE', Tool.objectTransformString(value, index + 1, mark))
          }
          str = str.replace('SITE_CONTENT_JSON', jsonStr)
          str = str.replace('SITE_JSON', Objects.SITE_JSON_CONTENT)
        }
        if (str === Objects.SITE_JSON) {
          str = '{}'
        } else {
          str = str.replace(Objects.SITE_JSON_TATIL, Objects.SITE_JSON_SAPCE)
          str = str.replace('SITE_SPACE', space)
        }
      }
    } else if (typeof content === 'string') {
      str = `'${content}'`
    } else {
      str = content
    }

    return str
  }

  static setSpace (index) {
    let result = ''
    for (let i = 0; i < index; i++) {
      result += '  '
    }
    return result
  }

  static refreshRouterTemplate (params) {
    let {dependence, routers, template} = params
    template = Templates.router.replace('SITE_DEPENDENCE_CONTENT', dependence)
    template = template.replace('SITE_ROUTERS_CONTENT', routers)
    template = template.replace('SITE_COMPONENT_FIELD', '')
    return template
  }
}

module.exports = Tool
