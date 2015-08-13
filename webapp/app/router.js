import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
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
  });

  this.route("test", { path: "/tests/:test_id" }, function() {
    this.route('errors');
    this.route('comments');
    this.route('activity');
  });

  this.resource('login', function() {});
  this.route('profile');
  this.route('user', { path: '/users/:user_id' });
  this.route('authorize-runtoken', { path: '/runtoken/:requestid/authorize' });


});

export default Router;
