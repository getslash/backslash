import { alias } from "@ember/object/computed";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import Controller from "@ember/controller";

export default Controller.extend({
  api: service(),
  admin_user_password_2: "",
  admin_user_password: alias("config.admin_user_password"),

  passwords_mismatch: computed(
    "admin_user_password",
    "admin_user_password_2",
    function() {
      return (
        this.get("admin_user_password") &&
        this.get("admin_user_password_2") &&
        this.get("admin_user_password") !== this.get("admin_user_password_2")
      );
    }
  ),

  password_classes: computed(
    "passwords_match",
    "passwords_mismatch",
    function() {
      let returned = "form-control ";
      if (this.get("passwords_mismatch")) {
        returned += "is-invalid";
      }
      return returned;
    }
  ),

  actions: {
    setup() {
      let self = this;
      self
        .get("api")
        .call("setup", {
          config: this.get("config"),
        })
        .then(function() {
          window.location.href = "/";
        });
    },
  },
});
