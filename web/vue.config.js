const webpack = require('webpack');

module.exports = {
  publicPath: '/',
  configureWebpack: {
    devServer: {
      contentBasePublicPath: '/',
      publicPath: '/',
      watchOptions: {
        ignored: [/node_modules/, /public/],
      },
    },
    plugins: [
      new webpack.DefinePlugin({
        'APP_NAME': JSON.stringify(require('./package.json').name),
      }),
    ],
  },
  devServer: {
    disableHostCheck: true,
  },
  lintOnSave: true,
};
