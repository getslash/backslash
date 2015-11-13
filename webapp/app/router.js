import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route("sessions", { path: "/sessions" });
  this.route("session", { path: "/sessions/:id" }, function() {
    this.route('tests');
    this.route('comments');
    this.route('errors');
    this.route('activity');
    this.route('investigate');
    this.route('warnings');
  });

  this.route("test", { path: "/tests/:test_id" }, function() {
    this.route('errors');
    this.route('comments');
    this.route('activity');
    this.route('warnings');
  });

  this.route('login', function() {});
  this.route('profile');
  this.route('user', { path: '/users/:email' }, function() {
    this.route('sessions');
    this.route('preferences');
  });
  this.route('authorize-runtoken', { path: '/runtoken/:requestid/authorize' });
  this.route('loading');
  this.route('users');
});

export default Router;

