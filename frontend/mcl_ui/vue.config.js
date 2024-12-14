const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  publicPath: '/',

  pages: {
    index: {
      entry: 'src/main.js',
      title: 'MCL UI',
    },
  },

  productionSourceMap: false,

  devServer: {
    port: 8080,
  },
});
