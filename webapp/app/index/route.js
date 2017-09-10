import Ember from "ember";

import BaseRoute from "../routes/base";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default BaseRoute.extend(AuthenticatedRouteMixin, {
  user_prefs: Ember.inject.service(),
  session: Ember.inject.service(),
  model() {
    return this.get("user_prefs").get_all();
  },

  afterModel(model) {
    if (model.start_page === "my sessions") {
      this.replaceWith(
        "user.sessions",
        this.get("session.data.authenticated.user_info.email")
      );
    } else {
      this.transitionTo("sessions", {
        queryParams: { page: 1, filter: undefined }
      });
    }
  }
});
