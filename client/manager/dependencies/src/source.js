const file = require('./file.js')
const tools = require('./tools.js')
const sources = require('../source/sources.js')

class Source {
  static get modules () {
    let modules = sources.modules
    let config = {}
    modules.forEach(item => {
      config[item.split('.')[0]] = item
    })
    return config
  }

  static get config () {
    let {components, config, modules} = sources
    components.forEach(item => {
      config.components[item] = false
    })
    modules.forEach(item => {
      config.modules[tools.firstChatUp(item.split('.')[0])] = false
    })
    return config
  }
}

module.exports = Source
