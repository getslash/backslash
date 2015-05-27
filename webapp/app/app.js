import Ember from 'ember';
import Resolver from 'ember/resolver';
import ApplicationSerializer from './serializers/application';
import loadInitializers from 'ember/load-initializers';
import config from './config/environment';

var App;

Ember.MODEL_FACTORY_INJECTIONS = true;

App = Ember.Application.extend({
  modulePrefix: config.modulePrefix,
  Resolver: Resolver
});

App.ApplicationSerializer = ApplicationSerializer;

loadInitializers(App, config.modulePrefix);

export default App;
