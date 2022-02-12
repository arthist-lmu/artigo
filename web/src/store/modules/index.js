const requireModule = require.context('.', false, /\.module\.js$/);
const modules = {};
requireModule.keys().forEach((fileName) => {
  const moduleName = fileName.replace(/(\.\/|\.module\.js)/g, '');
  modules[moduleName] = requireModule(fileName).default || requireModule(
    fileName,
  );
});

export default modules;
