import Ember from 'ember';
import Resolver from 'ember/resolver';
import ApplicationSerializer from './serializers/application';
import loadInitializers from 'ember/load-initializers';
import config from './config/environment';

Ember.MODEL_FACTORY_INJECTIONS = true;

var App = Ember.Application.extend({
  modulePrefix: config.modulePrefix,
  podModulePrefix: config.podModulePrefix,
  Resolver: Resolver
});

App.ApplicationSerializer = ApplicationSerializer;

loadInitializers(App, config.modulePrefix);

export default App;
