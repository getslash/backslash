import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  user_prefs: Ember.inject.service(),

  model: function() {
    return this.get("user_prefs").get_all();
  }
});
