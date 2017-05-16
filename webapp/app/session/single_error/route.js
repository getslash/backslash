import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  model: function(params) {
    let session = this.modelFor("session");

    return Ember.RSVP.hash({
      index: params.index,
      error: this.store.queryRecord("error", {
        session_id: session.id,
        page: params.index,
        page_size: 1
      }),
      session: this.store.find("session", session.id)
    });
  },

  setupController: function(controller, model) {
    this._super(controller, model);
    controller.setProperties(model);
  },

  renderTemplate: function() {
    this.render("single_error");
  }
});
