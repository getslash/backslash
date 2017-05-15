import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import RefreshableRouteMixin from "../mixins/refreshable-route";

export default Ember.Route.extend(
  AuthenticatedRouteMixin,
  RefreshableRouteMixin,
  {
    titleToken(model) {
      return `User ${model.get("email")}`;
    },

    model: function(params) {
      return this.store.findRecord("user", params.email, { reload: true });
    }
  }
);
