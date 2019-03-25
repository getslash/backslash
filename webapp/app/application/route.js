import { hash } from "rsvp";
import { inject as service } from "@ember/service";
import Route from "@ember/routing/route";
import ApplicationRouteMixin from "ember-simple-auth/mixins/application-route-mixin";
import config from "../config/environment";

export default Route.extend(ApplicationRouteMixin, {
  api: service(),
  session: service(),
  runtime_config: service(),
  user_prefs: service(),
  notifications: service("notification-messages"),

  title(tokens) {
    return tokens.join(" - ") + " - Backslash";
  },

  model() {
    return hash({
      runtime_config: this.get("runtime_config").get_all(),
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

  async sessionAuthenticated() {
    this._super(...arguments);
    await this.load_current_user();
  },

  async load_current_user() {
    let self = this;
    if (self.get("session.data.authenticated")) {
      let users = await self.store.query("user", { current_user: true });
      let user = await users.get("firstObject");

      self.set("session.data.authenticated.current_user", user);
      let alerts = await self.store.findAll("admin_alert");
      alerts.forEach(alert =>
        self.get("notifications").error(alert.get("message"))
      );
      return self.get("user_prefs").get_all();
    }
  },

  setupController(controller, model) {
    controller.setProperties(model);
    controller.set("version", model.runtime_config.version);
  },
});
