import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route("sessions", { path: "/sessions" });
  this.route("session", { path: "/sessions/:id" }, function() {
    this.route('errors');
    this.route('single_error', { path: "/sessions/:session_id/errors/:error_id" });
  });

  this.route("test", { path: "/tests/:test_id" }, function() {
    this.route('errors');
    this.route('single_error', { path: "/tests/:test_id/errors/:error_id" });
  });

  this.route('login', function() {});
  this.route('profile');
  this.route('user', { path: '/users/:email' }, function() {
    this.route('sessions');
    this.route('preferences');
  });
  this.route('authorize-pruntoken', { path: '/runtoken/:requestid/authorize' });
  this.route('loading');
  this.route('users');
});

export default Router;

