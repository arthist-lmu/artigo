const { VuetifyPlugin } = require('webpack-plugin-vuetify');
const webpack = require('webpack');
// const VuetifyLoaderPlugin = require('webpack-plugin-vuetify/lib/plugin');

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
      new VuetifyPlugin({ autoImport: true }),
      // new VuetifyLoaderPlugin({
      //   progressiveImage: {
      //     sharp: true,
      //   },
      // }),
    ],
    optimization: {
      splitChunks: {
        chunks: 'all',
        minSize: 10000,
        maxSize: 250000,
      },
    },
  },
  css: {
    loaderOptions: {
      sass: {
        implementation: require('sass'),
        additionalData: '@import \'@/styles/variables.scss\'',
      },
      scss: {
        additionalData: '@import \'@/styles/variables.scss\';',
      },
    },
  },
  devServer: {
    disableHostCheck: true,
  },
  lintOnSave: true,
};
