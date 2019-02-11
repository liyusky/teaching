const fs = require('fs')
const path = require('path')

const Vue_Path = path.join(__dirname, '../tempalte/vue.tempalte')
const Config_Path = path.join(__dirname, '../tempalte/config.tempalte')
const Router_Path = path.join(__dirname, '../tempalte/router.tempalte')


module.exports = {
  vue: fs.readFileSync(Vue_Path, 'utf8'),
  config: fs.readFileSync(Config_Path, 'utf8'),
  router: fs.readFileSync(Router_Path, 'utf8')
}
