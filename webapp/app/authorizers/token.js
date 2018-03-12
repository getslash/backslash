import { inject as service } from '@ember/service';
import Base from "ember-simple-auth/authorizers/base";

export default Base.extend({
  session: service(),
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
