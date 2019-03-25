import { hash } from "rsvp";
import BaseRoute from "../../routes/base";
import AuthenticatedRouteMixin from "ember-simple-auth/mixins/authenticated-route-mixin";
import ComplexModelRoute from "../../mixins/complex-model-route";
import { inject as service } from "@ember/service";

export default BaseRoute.extend(AuthenticatedRouteMixin, ComplexModelRoute, {
  infinity: service(),
  model: function() {
    const parent = this.modelFor("session").session_model;
    return hash({
      warnings: this.infinity.model("warning", {
        session_id: parent.id,
        modelPath: "controller.warnings",
      }),
    });
  },
});
