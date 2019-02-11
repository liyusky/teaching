const fs = require('fs')
const path = require('path')

const Tools_Path = path.join(__dirname, './tools.js')
const Source_Path = path.join(__dirname, './source.js')
const Templates_Path = path.join(__dirname, './template.js')

const Tools = require(Tools_Path)
const Sources = require(Source_Path)
const Templates = require(Templates_Path)

const args = {
  mark: 1,
  deep: -1
}

const Example = {}

class Config {
  static execute (params) {
    let {inner, outer, application} = params
    this.setConfig({
      dir: inner,
      type: false
    })
    args.deep = -1
    this.setConfig({
      dir: outer,
      type: true
    })
    args.deep = -1
    this.setConfig({
      dir: application,
      type: true
    })
  }

  static setConfig (params) {
    let {dir, type} = params
    args.deep += 1

    let sources = fs.readdirSync(dir, 'utf8')
    if (!(sources instanceof Array)) return console.log(sources)

    let name = path.basename(dir)
    let file = `${name}.config.js`

    if (args.deep < args.mark) return Tools.loop(Config.setConfig, {sources, ...params})
    if (sources.includes(file)) {
      Config.refreshConfig({
        type,
        name,
        address: path.join(dir, `${name}.config.js`),
      })
    }
    else {
      Config.initConfig({
        type: type,
        address: path.join(dir, `${name}.config.js`)
      })
    }
    return Tools.loop(Config.setConfig, {sources, ...params})
  }

  static initConfig (params) {
    let {type, address} = params
    let template = type ? Templates.outerConfig : Templates.innerConfig
    if (type) {
      delete template.example
    }
    else {
      delete template.router
      delete template.components
    }
    Tools.createFile(address, template, false)
  }

  static refreshConfig (params) {
    let {address, type, name} = params
    let config = this.setConfigJson(params)
    let template = Templates.refreshConfig({config, type})
    Tools.createFile(address, template, true)
  }

  static setConfigJson (params) {
    let {address, type, name} = params
    let currentConfig = require(address)
    let newConfig = {...Sources.config}

    newConfig.note = (typeof newConfig.note === 'string') ? currentConfig.note : ''

    newConfig.example = currentConfig.example
    Example[name] = currentConfig.example

    Object.keys(newConfig.source).forEach(item => {
      if (typeof currentConfig.source !== 'object') {
        newConfig.source[item] = Boolean(currentConfig.source)
      } else {
        newConfig.source[item] = currentConfig.source[item]
      }
    })

    Object.keys(newConfig.router).forEach(item => {
      if (typeof currentConfig.router !== 'object') {
        if (item === 'redirect') {
          newConfig.router[item] = false
        } else {
          newConfig.router[item] = Boolean(currentConfig.router)
        }
      } else {
        if (typeof currentConfig.router[item] === 'string') {
          newConfig.router[item] = `'${currentConfig.router[item]}'`
        } else {
          newConfig.router[item] = currentConfig.router[item]
        }
      }
    })

    Object.keys(newConfig.modules).forEach(item => {
      if (typeof currentConfig.modules !== 'object') {
        newConfig.modules[item] = Boolean(currentConfig.modules)
      } else {
        newConfig.modules[item] = currentConfig.modules[item]
      }
    })

    Object.keys(newConfig.components).forEach(item => {
      if (typeof currentConfig.components === 'object') {
        let content = currentConfig.components[item]
        if (typeof content === 'string') {
          newConfig.components[item] = `'${content}'`
        } else if (typeof content === 'object') {
          newConfig.components[item] = content
        } else if (typeof content === 'number' && content) {
          newConfig.components[item] = 1
        } else if (content) {
          if (Example[item]) {
            newConfig.components[item] = Example[item]
          } else {
            newConfig.components[item] = true
          }
        } else {
          newConfig.components[item] = false
        }
      }
    })

    if (type) {
      delete newConfig.example
    } else {
      delete newConfig.router
      delete newConfig.components
    }

    return newConfig
  }
}

module.exports = Config