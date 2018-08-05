import { alias, oneWay } from '@ember/object/computed';
import { inject as service } from '@ember/service';
import Controller from '@ember/controller';

export default Controller.extend({
  api: service(),
  user: alias("model.user"),
  tokens: oneWay("model.tokens"),
  session: service(),

  roles: function() {
    let user_roles = [];
    this.get("user.user_roles").forEach(role => user_roles.push(role.name));
    let returned = [];

    ["admin", "moderator", "proxy"].forEach(function(name) {
      returned.push({ name: name, enabled: user_roles.indexOf(name) !== -1 });
    });
    return returned;
  }.property("user.user_roles"),

  actions: {
    toggle: function(role) {
      let self = this;
      if (
        !self.get("session.data.authenticated.current_user.capabilities.admin")
      ) {
        return;
      }

      if (
        role === "admin" &&
        self.get("user.email") ===
          self.get("session.data.authenticated.user_info.email")
      ) {
        if (
          !window.confirm(
            "You are about to drop your own admin privileges. Are you sure?"
          )
        ) {
          return;
        }
      }
      self
        .get("api")
        .call("toggle_user_role", {
          user_id: parseInt(this.get("user.id")),
          role: role
        })
        .then(function() {
          self.get("user").reload();
        });
    }
  }
});
