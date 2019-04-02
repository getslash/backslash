/* global require, module */
/* eslint-env node */
'use strict';

const EmberApp = require('ember-cli/lib/broccoli/ember-app');
const mergeTrees = require('broccoli-merge-trees');

module.exports = function(/*defaults*/) {

  var app = new EmberApp({
    'ember-font-awesome': {
        useScss: true,
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

    'ember-bootstrap': {
      'bootstrapVersion': 4,
      'importBootstrapFont': false,
      'importBootstrapCSS': false
    }
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

  return mergeTrees([app.toTree()]);
};
