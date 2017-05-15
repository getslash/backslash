/* eslint-env node */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'webapp',
    environment: environment,
    rootURL: null,
    locationType: 'hash',
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {

	available_page_sizes: [25, 50, 100, 200],
	default_page_size: 25,

    },


    torii: {
        sessionServiceName: 'session',
        providers: {
            'google-oauth2': {
                // redirectUri is assigned in app.js...
                apiKey: null,
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
    ENV.rootURL = '/';
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};
