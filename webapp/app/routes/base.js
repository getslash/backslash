import Ember from "ember";

export default Ember.Route.extend({
  title: null,

  afterModel: function() {
    this.controllerFor("application").set("title", this.get("title"));
  }
});
