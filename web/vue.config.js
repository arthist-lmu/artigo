const webpack = require('webpack');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');

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
      new VuetifyLoaderPlugin({
        progressiveImage: {
          sharp: true,
        },
      }),
    ],
    optimization: {
      splitChunks: {
        chunks: 'all',
        minSize: 10000,
        maxSize: 250000,
      },
    },
  },
  devServer: {
    disableHostCheck: true,
  },
  lintOnSave: true,
};
