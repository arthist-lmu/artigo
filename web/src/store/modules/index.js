const modules = {}
const files = import.meta.glob('./*.module.js', { eager: true })
for (let [fileName, fileContent] of Object.entries(files)) {
  const moduleName = fileName.replace(/(\.\/|\.module\.js)/g, '')
  modules[moduleName] = fileContent.default || fileContent
}

export default modules
