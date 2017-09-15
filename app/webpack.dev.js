const webpack = require('webpack');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');
// const CleanObsoleteChunks = require('webpack-clean-obsolete-chunks');
module.exports = merge(common, {
  plugins: [
    // new CleanObsoleteChunks(),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('development')
      }
    })
  ]
});
