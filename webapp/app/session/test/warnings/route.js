import { hash } from "rsvp";
import { inject as service } from "@ember/service";
import BaseRoute from "../../../routes/base";
import AuthenticatedRouteMixin from "ember-simple-auth/mixins/authenticated-route-mixin";
import ComplexModelRoute from "../../../mixins/complex-model-route";

export default BaseRoute.extend(AuthenticatedRouteMixin, ComplexModelRoute, {
  infinity: service(),
  model: function() {
    const parent = this.modelFor("session.test").test_model;
    return hash({
      warnings: this.infinity.model("warning", {
        test_id: parent.id,
        modelPath: "controller.warnings",
      }),
    });
  },
});
