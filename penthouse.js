var penthouse = require('penthouse'),
    path = require('path'),
    fs = require('fs'),
    __basedir = './';

penthouse({
    url: 'https://www.varmedok.no/welcome',
    css: path.join(__basedir + 'static/css/main.css'),
    // OPTIONAL params
    width: 500,                    // viewport width
    height: 900,                    // viewport height
    forceInclude: [],
    timeout: 30000,                 // ms; abort critical CSS generation after this timeout
    strict: false,                  // set to true to throw on CSS errors (will run faster if no errors)
    maxEmbeddedBase64Length: 1000,  // characters; strip out inline base64 encoded resources larger than this
    userAgent: 'Penthouse Critical Path CSS Generator', // specify which user agent string when loading the page
    renderWaitTime: 100,            // ms; render wait timeout before CSS processing starts (default: 100)
    blockJSRequests: false,          // set to false to load (external) JS (default: true)
}, function(err, criticalCss) {
    if (err) {
        // handle error
        throw err;
    }

    fs.writeFileSync('outfile.css', criticalCss);
});
