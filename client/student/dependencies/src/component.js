const fs = require('fs')
const path = require('path')

const Templates_Path = path.join(__dirname, './template.js')
const Tools_Path = path.join(__dirname, './tools.js')

const Templates = require(Templates_Path)
const Tools = require(Tools_Path)

class Component {

  static execute (params) {
    let {inner, outer, application} = params
    Component.formatFile({dir: inner})
    Component.formatFile({dir: outer})
    Component.formatFile({dir: application})
  }


  static formatFile (params) {
    let { dir } = params
    let sources = fs.readdirSync(dir, 'utf8')
    if (!(sources instanceof Array)) return console.log(sources)

    let name = path.basename(dir)
    let file = `${name}.config.js`

    if (!sources.includes(file)) {
      console.log(`${dir} 下不存在 ${name}.config.js`)
      return Tools.loop(Component.formatFile, {sources, dir})
    }

    let config = require(path.join(dir, file))
    Component.manageFile({config, sources, dir, name})

    return Tools.loop(Component.formatFile, {sources, dir})
  }

  static manageFile (params) {
    let {config, config: {source}, sources, name, dir, template} = params
    for (let [style, active] of Object.entries(source)) {
      if (!active) continue
      let fileName = `${name}.${style}`
      let refresh = sources.includes(fileName)
      let address = path.join(dir, fileName)
      switch (style) {
        case 'scss':
          template = Templates.scss({address, name, refresh})
          break
        case 'js':
          template = Templates.js({address, name, refresh})
          break
        case 'vue':
          template = Templates.vue({config, address, name, refresh})
          break
      }
      Tools.createFile(address, template, refresh)
    }
  }

  static components () {
  }
}

module.exports = Component