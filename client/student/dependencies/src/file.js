const fs = require('fs')
class Files {
  static create (path, content, refresh) {
    let result = fs.writeFileSync(path, content)
    let state = '创建'
    if (refresh) state = '更新'
    let logStr = `${path} ${state}成功`
    if (result) {
      logStr = `${path} ${state}失败 ===== ${result}`
    }
  }
}
module.exports = Files