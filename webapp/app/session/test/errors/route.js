import Ember from "ember";
import AuthenticatedRouteMixin
  from "ember-simple-auth/mixins/authenticated-route-mixin";
import InfinityRoute from "../../../mixins/infinity-route";
import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Ember.Route.extend(
  AuthenticatedRouteMixin,
  InfinityRoute,
  ComplexModelRoute,
  {
    model: function() {
      const parent = this.modelFor("session.test");
      return Ember.RSVP.hash({
        test_model: parent.test_model,
        session_model: parent.session_model,
        errors: this.infinityModel("error", {
          test_id: parent.test_model.id,
          modelPath: "controller.errors"
        })
      });
    }
  }
);
