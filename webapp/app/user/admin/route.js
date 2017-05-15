import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  api: Ember.inject.service(),
  needs: "user",

  model: function() {
    return new Ember.RSVP.hash({
      user: this.modelFor("user"),
      tokens: this.get("api").call("get_user_run_tokens", {
        user_id: parseInt(this.modelFor("user").id)
      })
    });
  }
});
