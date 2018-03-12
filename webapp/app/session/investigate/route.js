import Route from '@ember/routing/route';

export default Route.extend({
  needs: ["session"],

  model: function() {
    return this.modelFor("session");
  }
});
