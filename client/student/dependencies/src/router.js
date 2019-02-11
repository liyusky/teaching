const fs = require('fs')
const path = require('path')

const Params_Path = path.join(__dirname, '../source/params.js')
const Tools_Path = path.join(__dirname, './tools.js')

const { Router } = require(Params_Path)
const Tools = require(Tools_Path)
const RouterContent = []
const RouterPath = {
  content: [],
  children: {}
}

let firstMark = false

const Template = {
  component: 'SITE_COMPONENT_FIELD'
}

class Routers {
  static execute (dir, address) {
    Routers.getRouterMessage({
      dir,
      father: RouterPath,
      router: RouterContent
    })
    Routers.formatRouter(RouterContent)
    let template = Tools.refreshRouterTemplate({
      dependence: Template.component,
      routers: Tools.objectTransformString(RouterContent, 1, true)
    })
    Tools.createFile(address, template, true)
  }

  static getRouterMessage (params) {
    let { dir } = params
    let router = params.router
    let father = params.father
    let sources = fs.readdirSync(dir, 'utf8')
    if (!(sources instanceof Array)) return console.log(sources)
    let name = path.basename(dir)
    let file = `${name}.config.js`
    if (!sources.includes(file)) {
      if (firstMark) console.log(`${dir} 下不存在 ${name}.config.js`)
      firstMark = true
      return Tools.loop(Routers.getRouterMessage, { sources, dir, father, router })
    }
    let config = require(path.join(dir, file))
    let address = path.join(dir, `${name}.vue`)
    let { alias, redirect, component, home } = config.router
    let result = Routers.setRouterPath(father, name)
    if (alias || redirect || component) {
      router = Routers.setRouterContent({ paths: result.paths, router, alias, name, address, redirect, component, home })
      return Tools.loop(Routers.getRouterMessage, { sources, dir, father: result.father, router })
    }
  }

  static setRouterContent (params) {
    let { paths, alias, name, address, redirect, component, home } = params
    let config = {
      path: home ? '/' : this.setPath(paths),
      name: this.setAlias(alias, paths),
      component: this.setRouterDependence(name, alias, paths, address, component),
      children: []
    }
    if (redirect) config.redirect = this.setRedirect(address, redirect)

    params.router.push(config)
    return config.children
  }

  static formatRouter (params) {
    params.forEach(item => {
      if (item.children.length) {
        return Routers.formatRouter(item.children)
      } else {
        delete item.children
      }
    })
  }

  static setRouterDependence (name, alias, content, address, component) {
    Template.component = Template.component.replace('SITE_COMPONENT_FIELD', Router.SITE_COMPONENT_FIELD)
    Template.component = Template.component.replace('SITE_NAME', this.setChunkName(alias, content))
    let relativePath = ''
    switch (typeof component) {
      case 'boolean':
        relativePath = Tools.getRelativePath(address)
        break
      case 'string':
        relativePath = Tools.getRelativePath(component)
        name = path.basename(component)
    }
    Template.component = Template.component.replace('SITE_COMPONENT_NAME', Tools.setComponentsName(name))
    Template.component = Template.component.replace('SITE_COMPONENT_PATH', relativePath.replace(/\\/g, '/'))
    return Tools.setComponentsName(name)
  }

  static setPath (content) {
    return `/${content.join('/')}`
  }

  static setAlias (alias, content) {
    if (typeof alias === 'boolean') alias = content.join('-')
    return alias
  }

  static setChunkName (alias, content) {
    if (typeof alias === 'string') {
      content.pop()
      content.push(alias)
    }
    return content.join('-')
  }

  static setRedirect (address, redirect) {
    let content = path.relative(address, redirect).split('\\')
    content.pop()
    console.log(content.join('/'))
    return content.join('/').replace(/[../]*/, '/')
  }

  static setRouterPath (father, name) {
    father.children[name] = {
      content: [],
      children: {}
    }
    father.children[name].content = [...father.content]
    father.children[name].content.push(name)
    return {
      paths: father.children[name].content,
      father: father.children[name]
    }
  }
}

module.exports = Routers
