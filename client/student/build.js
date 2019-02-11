const fs = require('fs')
const path = require('path')

const Config = require('./dependencies/src/config.js')
const Component = require('./dependencies/src/component.js')
const Routers = require('./dependencies/src/router.js')

const inner = path.join(__dirname, './dependencies/components')
const outer = path.join(__dirname, './src/components')
const application = path.join(__dirname, './src/app')

const Pages = path.join(__dirname, './src/components')
const RouterPath = path.join(__dirname, './src/router/router.js')

Config.execute({inner, outer, application})
Component.execute({inner, outer, application})
Routers.execute(Pages, RouterPath)