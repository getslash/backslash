import Route from '@ember/routing/route';

export default Route.extend({
  title: null,

  afterModel: function() {
    this.controllerFor("application").set("title", this.get("title"));
  }
});
