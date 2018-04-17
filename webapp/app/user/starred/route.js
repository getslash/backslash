import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
export default Route.extend(AuthenticatedRouteMixin, {

  model() {
    return this.store
      .query("test", {starred: true})
      .then(function(tests) {
        return { tests: tests, error: null};
      })
      .catch(function(exception) {
        return {error: exception.errors.get('firstObject')};
      });
  },

  setupController(controller, model) {
    this._super(...arguments);
    controller.setProperties(model);
  },
});
