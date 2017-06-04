import Ember from "ember";

import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Ember.Route.extend(ComplexModelRoute, {

  model() {
    let session_model = this.modelFor("session").session_model;
    let test_model = this.modelFor("session.test").test_model;
    let test_metadata = this.modelFor("session.test").test_metadata;
    return Ember.RSVP.hash({
      session_model: session_model,
      test_model: test_model,
      metadata: test_metadata,
    });
  }
});
