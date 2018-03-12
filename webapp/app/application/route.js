import { hash } from 'rsvp';
import { inject as service } from '@ember/service';
import Route from '@ember/routing/route';

import retry from "ember-retry/retry";

import ApplicationRouteMixin
  from "ember-simple-auth/mixins/application-route-mixin";
import config from "../config/environment";

export default Route.extend(ApplicationRouteMixin, {
  api: service(),
  session: service(),
  runtime_config: service(),
  user_prefs: service(),

  title(tokens) {
    return tokens.join(" - ") + " - Backslash";
  },

  model() {
    return hash({
      runtime_config: this.get("runtime_config").get_all()
    });
  },

  afterModel(model) {
    if (model.runtime_config.setup_needed) {
      this.transitionTo("setup");
    } else {
      let cfg = config.torii;
      cfg.providers["google-oauth2"].apiKey =
        model.runtime_config.google_oauth2_client_id;
      this.load_current_user();
    }
  },

  sessionAuthenticated() {
    this._super(...arguments);
    this.load_current_user();
  },

  load_current_user() {
    let self = this;
    if (self.get("session.data.authenticated")) {
      return retry(async function() {
        let users = await self.store.query("user", {current_user: true});
        let user = await users.get('firstObject');
        self.set("session.data.authenticated.current_user", user);
        return self.get("user_prefs").get_all();
      });
    }
  },

  setupController(controller, model) {
    controller.setProperties(model);
    controller.set("version", model.runtime_config.version);
  }
});
