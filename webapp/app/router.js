import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
    this.route("sessions", { path: "/sessions" });
    this.route("session", { path: "/sessions/:id" });

    this.route("tests", { path: "/tests" });
    this.resource("test", { path: "/tests/:test_id" });

    this.route('search-sessions', { path: '/sessions/search/:filters' });
    this.route('search-tests', { path: '/tests/search/:filters' });
    this.resource('setup', function() {});
    this.resource('login', function() {});
    this.route('debug');
    this.route('profile');
    this.route('user', { path: '/users/:user_id' });
    this.route('authorize-runtoken', { path: '/runtoken/:requestid/authorize' });


});

export default Router;
