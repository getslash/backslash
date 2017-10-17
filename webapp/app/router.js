import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route("index", { path: "/" });
  this.route("sessions", { path: "/sessions" });
  this.route("session", { path: "/sessions/:id" }, function() {
    this.route("interruptions");
    this.route("errors");
    this.route("single_error", { path: "/errors/:index" });
    this.route("warnings");
    this.route("info");
    this.route("children");
    this.route("test", {path: "/tests/:test_id"}, function() {
      this.route("interruptions");
      this.route("errors");
      this.route("warnings");
      this.route("comments");
    });
    this.route("comments");
  });

  this.route("test", { path: "/tests/:test_id" }, function() {
    this.route("comments");
  });

  this.route("login", function() {});
  this.route("profile");
  this.route("user", { path: "/users/:email" }, function() {
    this.route("sessions");
    this.route("admin");
    this.route("preferences");
  });
  this.route("authorize-runtoken", { path: "/runtoken/:requestid/authorize" });
  this.route("users");
  this.route("subjects");
  this.route("subject", { path: "/subjects/:name" });
  this.route("component-proofing");
  this.route("setup");
  this.route("not-found", { path: "/*:unknown" });
  this.route("tests");

  this.route('admin', function() {
    this.route('migrations');
  });
  this.route('cases');
});

export default Router;
