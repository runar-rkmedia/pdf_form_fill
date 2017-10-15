var webpack = require('webpack'),
  path = require('path'),
  srcPath = path.join(__dirname, 'src'),
  genOutPath = path.join('static', 'gen'),
  ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');
// TODO: serve kncokout.validation from CDN instead of bundling it.
const AssetsPlugin = require('assets-webpack-plugin')
const assetsPluginInstance = new AssetsPlugin()
const ExtractTextPlugin = require("extract-text-webpack-plugin");

const extractLess = new ExtractTextPlugin({
  filename: path.join(genOutPath, "style.[hash].css"),
  disable: process.env.NODE_ENV === "development"
});
module.exports = {
  context: __dirname, // to automatically find tsconfig.json
  target: 'web',
  cache: true,
  entry: path.join(srcPath, "/main.ts"),
  output: {
    filename: path.join(genOutPath, "/vk_app.[hash].js"),
  },
  externals: {
    // require("jquery") is external and available
    //  on the global var jQuery
    "jquery": 'jQuery',
    "knockout": 'ko',
    // "knockout.validation": 'kv',
    "webfontloader": 'WebFont',
    "bootbox": 'bootbox',
    "moment": 'moment',
    // "kv": 'knockout_validation'
  },
  resolve: {
    // Add '.ts' and '.tsx' as a resolvable extension.
    extensions: ["*", ".webpack.js", ".web.js", ".ts", '.js', '.jsx']
  },
  module: {
    loaders: [
      { test: /\.html$/, loader: "raw-loader" },
      // all files with a '.ts' or '.tsx' extension will be handled by 'ts-loader'
      {
        test: /\.tsx?$/,
        loader: "ts-loader",
        include: srcPath,
        options: {
          // disable type checker - we will use it in fork plugin
          transpileOnly: true
        }
      },
      {
        test: /\.less$/,
        use: extractLess.extract({
          use: [{
            loader: "css-loader"
          }, {
            loader: "less-loader"
          }],
          // use style-loader in development
          fallback: "style-loader"
        })
      },
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader'
      },
      {
        test: /\.png$/,
        loader: 'url-loader?limit=100000'
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff',
        options: {
          publicPath: 'static/',
          outputPath: 'static/'
        }
      },
      {
        test: /\.(ttf|otf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?|(jpg|gif)$/,
        loader: 'file-loader',
        options: {
          publicPath: 'static/',
          outputPath: 'static/'
        }
      }
    ]
  },
  plugins: [
    extractLess,
    assetsPluginInstance
  ]
};
