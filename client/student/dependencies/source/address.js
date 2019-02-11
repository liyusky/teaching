const path = require('path')

module.exports = {
  modulesJson: path.join(__dirname, './modules.js'),
  modules: path.join(__dirname, '../modules'),
  flex: path.join(__dirname, '../sass/_flex.scss'),
  unit: path.join(__dirname, '../sass/_unit.scss'),
  components: path.join(__dirname, '../components')
}
