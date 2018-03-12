import { hash } from 'rsvp';
import { inject as service } from '@ember/service';
import Route from '@ember/routing/route';
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";

export default Route.extend(AuthenticatedRouteMixin, {
  api: service(),
  needs: "user",

  model: function() {
    return new hash({
      user: this.modelFor("user"),
      tokens: this.get("api").call("get_user_run_tokens", {
        user_id: parseInt(this.modelFor("user").id)
      })
    });
  }
});
