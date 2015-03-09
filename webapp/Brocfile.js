/* global require, module */

var EmberApp = require('ember-cli/lib/broccoli/ember-app');

var app = new EmberApp({
    vendorFiles: {
        'handlebars.js': null
    }});

// Use `app.import` to add additional libraries to the generated
// output files.
//
// If you need to use different assets in different
// environments, specify an object as the first parameter. That
// object's keys should be the environment name and the values
// should be the asset to use in that environment.
//
// If the library that you are including contains AMD or ES6
// modules that you would like to import into your application
// please specify an object with the list of modules as keys
// along with the exports of each module as its value.

var mergeTrees = require('broccoli-merge-trees');
var pickFiles = require('broccoli-static-compiler');

var fontTree = pickFiles('bower_components/fontawesome/fonts', {
  srcDir: '/',
  files: ['fontawesome-webfont.eot','fontawesome-webfont.ttf','fontawesome-webfont.svg','fontawesome-webfont.woff'],
  destDir: '/assets/fonts'
});

var cssTree = pickFiles('bower_components/fontawesome/css', {
  srcDir: '/',
  files: ['font-awesome.min.css'],
  destDir: '/assets/css'
});

app.import('bower_components/jquery-treegrid/css/jquery.treegrid.css');
app.import('bower_components/jquery-treegrid/js/jquery.treegrid.js');
app.import('bower_components/jquery-treegrid/img/collapse.png', {
  destDir: '/img'
});
app.import('bower_components/jquery-treegrid/img/expand.png', {
  destDir: '/img'
});

var images = pickFiles('public/assets/img', {
  srcDir: '/',
  files: ['*'],
  destDir: '/img'
});
module.exports = mergeTrees([app.toTree(), fontTree, cssTree, images]);
