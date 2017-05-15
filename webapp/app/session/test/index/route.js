import Ember from "ember";

import ComplexModelRoute from "../../../mixins/complex-model-route";

export default Ember.Route.extend(ComplexModelRoute, {
  api: Ember.inject.service(),

  model() {
    let session_model = this.modelFor("session").session_model;
    let test_model = this.modelFor("session.test").test_model;
    return Ember.RSVP.hash({
      session_model: session_model,
      test_model: test_model,
      metadata: this.get("api")
        .call("get_metadata", {
          entity_type: "test",
          entity_id: parseInt(test_model.id)
        })
        .then(r => r.result)
    });
  }
});
