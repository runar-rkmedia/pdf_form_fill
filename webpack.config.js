var webpack = require('webpack'),
  path = require('path'),
  srcPath = path.join(__dirname, 'src'),
  jsOutPath = path.join('static', 'js'),
  UglifyJSPlugin = require('uglifyjs-webpack-plugin'),
  ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');
// TODO: serve kncokout.validation from CDN instead of bundling it.

module.exports = {
  // context: __dirname, // to automatically find tsconfig.json
  target: 'web',
  cache: true,
  entry: path.join(srcPath, "/main.ts"),
  output: {
    filename: path.join(jsOutPath, "/main.js")
  },
  externals: {
    // require("jquery") is external and available
    //  on the global var jQuery
    "jquery": 'jQuery',
    "knockout": 'ko',
    // "kv": 'knockout_validation'
  },
  resolve: {
    // Add '.ts' and '.tsx' as a resolvable extension.
    extensions: ["*", ".webpack.js", ".web.js", ".ts", '.js', '.jsx']
  },
  module: {
    loaders: [
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
        use: [{
          loader: "style-loader" // creates style nodes from JS strings
        }, {
          loader: "css-loader" // translates CSS into CommonJS
        }, {
          loader: "less-loader" // compiles Less to CSS
        }]
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
    // new UglifyJSPlugin(),
    new ForkTsCheckerWebpackPlugin()
  ]
}
