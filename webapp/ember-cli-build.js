/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {

  var app = new EmberApp({
      'ember-font-awesome': {
          useScss: true,
      },
      'ember-cli-bootstrap-sassy': {
          'quiet': true
      },
      'ember-cli-tooltipster': {
          importTooltipsterBorderless: true
      },
      vendorFiles: {
          'handlebars.js': null
      },
      'ember-cli-babel': {
          includePolyfill: true,
      },
  });

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
  app.import('bower_components/js-md5/js/md5.min.js');
  app.import('bower_components/moment/moment.js');
  app.import('bower_components/twix/dist/twix.min.js')
  app.import('bower_components/Heyoffline/heyoffline.js')


  var mergeTrees = require('broccoli-merge-trees');
  var pickFiles = require('broccoli-static-compiler');

  var images = pickFiles('public/assets/img', {
      srcDir: '/',
      files: ['*'],
      destDir: '/img'
  });

  return mergeTrees([app.toTree(), images]);
};
