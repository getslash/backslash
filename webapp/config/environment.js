/* jshint node: true */

var spawnSync = require('child_process').spawnSync;


module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'webapp',
    environment: environment,
    baseURL: '/',
    locationType: 'hash',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },

    torii: {
        sessionServiceName: 'session',
        providers: {
            'google-oauth2': {
                // redirectUri is assigned in app.js...
                apiKey: '705802534104-f01f9db07j8dvl4l9tp6nhc7keciamer.apps.googleusercontent.com',
                scope: 'email profile'
            }
        }
    }
  };

  ENV['ember-simple-auth'] = {
      authorizer: 'authorizer:token',
      store: 'session-store:local-storage'
  };

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.baseURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  ENV.app_version = '?';
  if (spawnSync !== undefined) {
    var result = spawnSync('git', ['describe', '--tags']);
    if (result.status !== 0) {
      throw new Error('Git returned with status ' + result.status + ': ' +
              result.stderr.toString().trim());
    }
    ENV.app_version = result.stdout.toString().trim();
  }
  
  return ENV;
};
