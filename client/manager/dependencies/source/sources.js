const fs = require('fs')
const path = require('path')

const Components_Path = path.join(__dirname, '../components')
const Modules_Path = path.join(__dirname, '../modules')
const Config_Path = path.join(__dirname, './config.js')

let components = fs.readdirSync(Components_Path, 'utf8')
let modules = fs.readdirSync(Modules_Path, 'utf8')
let config = require(Config_Path)

module.exports = {
  components,
  modules,
  config
}