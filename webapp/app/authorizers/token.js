import Ember from "ember";
import Base from "ember-simple-auth/authorizers/base";

export default Base.extend({
  session: Ember.inject.service(),
  authorize: function(jqXHR, requestOptions) {
    var session = this.get("session");
    if (!session.isAuthenticated) {
      return;
    }

    var auth_token = session.content.auth_token;
    if (requestOptions.headers === undefined) {
      requestOptions.headers = {};
    }

    requestOptions.headers["Authentication-Token"] = auth_token;
  }
});
