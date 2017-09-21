const webpack = require('webpack');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
// const PurifyCSSPlugin = require('purifycss-webpack');
const glob = require('glob');
const path = require('path');
module.exports = merge(common, {
  plugins: [
    new UglifyJSPlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }
    }),
    new OptimizeCssAssetsPlugin({
      // assetNameRegExp: /\.optimize\.css$/g,
      cssProcessor: require('cssnano'),
      cssProcessorOptions: {
        discardComments: {
          removeAll: true
        }
      },
      canPrint: true
    })
    // new PurifyCSSPlugin({
    //   // Give paths to parse for rules. These should be absolute!
    //   paths: glob.sync(
    //     path.join(__dirname, 'templates/**/*.html'),
    //     path.join(__dirname, 'static/js/*.js'),
    //     path.join(__dirname, 'src/**/*.*')
    //   ),
    //   purifyOptions: {
    //     rejected: true,
    //     whitelist: ['*bootstrap-datetimepicker*', '*fieldset*"', '*panel*']
    //   }
    // })
  ]
});
